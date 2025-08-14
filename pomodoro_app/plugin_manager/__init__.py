from __future__ import annotations

from pathlib import Path
from typing import Dict

from pomodoro_app.infrastructure.i18n import DOMAIN as CORE_DOMAIN


_plugin_domains: Dict[str, Path] = {}


def register_plugin_domain(name: str, locales_path: Path) -> None:
    """Register a plugin gettext domain and its locales path.

    Plugins can call this during load to have their catalogs available for lookup.
    """

    _plugin_domains[name] = locales_path


def get_plugin_domains() -> Dict[str, Path]:
    return dict(_plugin_domains)


__all__ = ["register_plugin_domain", "get_plugin_domains", "CORE_DOMAIN"]


