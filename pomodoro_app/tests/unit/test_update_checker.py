from __future__ import annotations

import json
import time
from pathlib import Path

from pomodoro_app.infrastructure.update.checker import (
    get_cache_path,
    read_cache,
    write_cache,
    is_cache_fresh,
    is_newer_version,
    UpdateChecker,
)


def test_cache_read_write_and_freshness(tmp_path: Path, monkeypatch: object) -> None:
    # Redirect user_data_dir via HOME to tmp
    monkeypatch.setenv("HOME", str(tmp_path))

    cache_path = get_cache_path()
    assert cache_path.parent.exists()

    write_cache({"last_checked": time.time(), "last_result": {"version": "0.2.0"}})
    cache = read_cache()
    assert is_cache_fresh(cache)


def test_is_newer_version_semver() -> None:
    assert is_newer_version("0.1.0", "0.2.0") is True
    assert is_newer_version("0.2.0", "0.1.0") is False


def test_update_checker_skips_when_fresh(tmp_path: Path, monkeypatch: object) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    cache_path = get_cache_path()
    write_cache({"last_checked": time.time(), "last_result": {"version": "9.9.9"}})

    uc = UpdateChecker(url="http://invalid.local/does-not-matter")
    result = uc.check_now(force=False)
    assert result == {"version": "9.9.9"}


