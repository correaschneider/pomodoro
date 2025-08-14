from __future__ import annotations

from packaging.version import Version
from packaging.specifiers import SpecifierSet


def is_compatible(app_version: str, spec: str) -> bool:
    """Return True if app_version satisfies the given specifier string."""

    try:
        v = Version(app_version)
        s = SpecifierSet(spec)
        return v in s
    except Exception:
        return False


__all__ = ["is_compatible"]


