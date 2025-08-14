from __future__ import annotations

from pomodoro_app.infrastructure.update.checker import is_newer_version


def test_versioning_and_prereleases() -> None:
    assert is_newer_version("1.0.0", "1.0.1") is True
    assert is_newer_version("1.0.1", "1.0.0") is False

    # pre-releases should not trigger by default
    assert is_newer_version("1.0.0", "1.1.0rc1") is False


