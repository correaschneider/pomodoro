from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Iterable, List, Tuple, Dict, Any

import pluggy
from platformdirs import user_data_dir

from pomodoro_app.infrastructure.logging import get_logger
from pomodoro_app import __version__ as APP_VERSION
from .metadata import load_plugin_metadata, PluginMetadata
from .semver import is_compatible
from .spec import PROJECT_NAME, hookspec


logger = get_logger("pomodoro.plugin.manager")
plugin_err_logger = get_logger("plugin")

# In-memory registry for auditing purposes
_plugin_registry: List[Dict[str, Any]] = []


def get_plugins_base_dir(app_name: str = "pomodoro_app") -> Path:
    """Return the base directory where user plugins are discovered."""

    return Path(user_data_dir(app_name)) / "plugins"


def discover_plugin_folders(base_dir: Path | None = None) -> List[Path]:
    """Discover plugin folders containing at least a main.py file.

    A valid plugin folder layout is expected to be:
      <plugin_dir>/plugin.toml (optional at this stage)
      <plugin_dir>/main.py      (required)
    """

    root = base_dir or get_plugins_base_dir()
    if not root.exists():
        return []
    plugins: List[Path] = []
    for entry in root.iterdir():
        if not entry.is_dir():
            continue
        main_py = entry / "main.py"
        if main_py.is_file():
            plugins.append(entry)
    return plugins


def create_plugin_manager() -> pluggy.PluginManager:
    """Create a Pluggy PluginManager preconfigured with our hookspecs."""

    pm = pluggy.PluginManager(PROJECT_NAME)
    pm.add_hookspecs(__import__("pomodoro_app.plugin_manager.spec", fromlist=["spec"]))
    return pm


def _load_module_from_path(module_name: str, path: Path):
    spec = spec_from_file_location(module_name, str(path))
    if spec is None or spec.loader is None:  # type: ignore[truthy-bool]
        raise ImportError(f"cannot load plugin module from {path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[assignment]
    return module


def load_and_register_plugins(pm: pluggy.PluginManager, base_dir: Path | None = None) -> Tuple[int, int]:
    """Discover, validate and register plugins.

    Returns (loaded_count, skipped_count).
    """

    loaded = 0
    skipped = 0
    for folder in discover_plugin_folders(base_dir):
        try:
            meta = load_plugin_metadata(folder)
        except Exception:
            logger.exception("invalid plugin metadata in %s", folder)
            plugin_err_logger.error("invalid plugin metadata in %s", folder)
            skipped += 1
            continue

        if not is_compatible(APP_VERSION, meta.plugin.compatible_with):
            logger.info(
                "skip plugin %s due to incompatible spec %s",
                meta.plugin.name,
                meta.plugin.compatible_with,
            )
            plugin_err_logger.error(
                "incompatible plugin %s (requires %s)", meta.plugin.name, meta.plugin.compatible_with
            )
            skipped += 1
            continue

        # Security: skip GUI-only plugin if GUI not available
        if meta.access.requires_gui and not _is_gui_available():
            logger.info("skip GUI-only plugin %s: GUI not available", meta.plugin.name)
            plugin_err_logger.error("GUI not available for plugin %s", meta.plugin.name)
            _record_registry(meta, folder, status="skipped", reason="no-gui")
            skipped += 1
            continue

        main_py = folder / "main.py"
        try:
            module_name = f"plugin_{meta.plugin.name}"
            module = _load_module_from_path(module_name, main_py)
            pm.register(module)
            logger.info("registered plugin %s", meta.plugin.name)
            _record_registry(meta, folder, status="loaded", reason=None)
            loaded += 1
        except Exception:
            logger.exception("failed to load/register plugin at %s", main_py)
            plugin_err_logger.error("failed to load/register plugin at %s", main_py)
            _record_registry(meta, folder, status="skipped", reason="load-error")
            skipped += 1
    return loaded, skipped


def _is_gui_available() -> bool:
    try:
        from PySide6 import QtWidgets  # type: ignore

        return QtWidgets.QApplication.instance() is not None
    except Exception:
        return False


def _record_registry(meta: PluginMetadata, folder: Path, status: str, reason: str | None) -> None:
    _plugin_registry.append(
        {
            "name": meta.plugin.name,
            "version": meta.plugin.version,
            "compatible_with": meta.plugin.compatible_with,
            "access": {
                "filesystem": meta.access.filesystem,
                "network": meta.access.network,
                "requires_gui": meta.access.requires_gui,
            },
            "folder": str(folder),
            "status": status,
            "reason": reason,
        }
    )


def get_plugin_registry() -> List[Dict[str, Any]]:
    return list(_plugin_registry)


__all__ = [
    "get_plugins_base_dir",
    "discover_plugin_folders",
    "create_plugin_manager",
    "load_and_register_plugins",
    "get_plugin_registry",
]


