from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.plugin.metadata")


@dataclass(frozen=True)
class PluginInfo:
    name: str
    version: str
    compatible_with: str


@dataclass(frozen=True)
class AccessInfo:
    filesystem: bool = False
    network: bool = False
    requires_gui: bool = False


@dataclass(frozen=True)
class PluginMetadata:
    plugin: PluginInfo
    access: AccessInfo


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _simple_toml_parse(text: str) -> Dict[str, Dict[str, Any]]:
    """Very small TOML subset parser for our plugin.toml needs.

    Supports:
      - Sections: [plugin], [access]
      - key = "string" or key = true/false
    """

    data: Dict[str, Dict[str, Any]] = {}
    section = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1].strip()
            if section not in data:
                data[section] = {}
            continue
        if "=" in line and section is not None:
            k, v = line.split("=", 1)
            key = k.strip()
            val = v.strip()
            if val.startswith('"') and val.endswith('"'):
                data[section][key] = val[1:-1]
            elif val.lower() in {"true", "false", "1", "0", "yes", "no", "on", "off"}:
                data[section][key] = _parse_bool(val)
            else:
                data[section][key] = val
    return data


def load_plugin_metadata(plugin_dir: Path) -> PluginMetadata:
    """Read and validate plugin.toml metadata from a plugin directory.

    Raises ValueError on invalid or missing required fields.
    """

    toml_path = plugin_dir / "plugin.toml"
    if not toml_path.exists():
        raise ValueError(f"plugin.toml not found in {plugin_dir}")

    try:
        text = toml_path.read_text(encoding="utf-8")
        raw = _simple_toml_parse(text)
    except Exception as exc:
        logger.exception("Failed to read/parse plugin.toml: %s", exc)
        raise ValueError("invalid plugin.toml") from exc

    plugin_sec = raw.get("plugin", {})
    access_sec = raw.get("access", {})

    # Required fields
    name = str(plugin_sec.get("name", "")).strip()
    version = str(plugin_sec.get("version", "")).strip()
    compatible_with = str(plugin_sec.get("compatible_with", "")).strip()
    if not name or not version or not compatible_with:
        raise ValueError("plugin metadata missing required fields: name/version/compatible_with")

    plugin = PluginInfo(name=name, version=version, compatible_with=compatible_with)

    access = AccessInfo(
        filesystem=bool(access_sec.get("filesystem", False)),
        network=bool(access_sec.get("network", False)),
        requires_gui=bool(access_sec.get("requires_gui", False)),
    )

    return PluginMetadata(plugin=plugin, access=access)


__all__ = [
    "PluginInfo",
    "AccessInfo",
    "PluginMetadata",
    "load_plugin_metadata",
]


