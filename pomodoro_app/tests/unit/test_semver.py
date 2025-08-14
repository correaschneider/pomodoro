from __future__ import annotations

from pomodoro_app.plugin_manager.semver import is_compatible


def test_is_compatible_basic() -> None:
    assert is_compatible("1.2.3", ">=1.0.0") is True
    assert is_compatible("0.9.0", ">=1.0.0") is False


