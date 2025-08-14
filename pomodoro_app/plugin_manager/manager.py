from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Iterable, List

import pluggy
from platformdirs import user_data_dir

from pomodoro_app.infrastructure.logging import get_logger
from .spec import PROJECT_NAME, hookspec


logger = get_logger("pomodoro.plugin.manager")


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


__all__ = [
    "get_plugins_base_dir",
    "discover_plugin_folders",
    "create_plugin_manager",
]


