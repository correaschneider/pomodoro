from __future__ import annotations

import json
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from platformdirs import user_data_dir

from packaging.version import Version

from pomodoro_app.infrastructure.logging import get_logger
from pomodoro_app import __version__ as APP_VERSION


logger = get_logger("pomodoro.infrastructure.update")

DEFAULT_UPDATE_URL = "https://example.com/pomodoro_app/update.json"
CACHE_FILE_NAME = "update_cache.json"
ONE_DAY_SECONDS = 24 * 60 * 60


def get_cache_path(app_name: str = "pomodoro_app") -> Path:
    base = Path(user_data_dir(app_name)) / "cache"
    base.mkdir(parents=True, exist_ok=True)
    return base / CACHE_FILE_NAME


def read_cache(cache_path: Optional[Path] = None) -> Dict[str, Any]:
    path = cache_path or get_cache_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        logger.exception("Failed to read update cache; ignoring")
        return {}


def write_cache(data: Dict[str, Any], cache_path: Optional[Path] = None) -> None:
    path = cache_path or get_cache_path()
    try:
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    except Exception:
        logger.exception("Failed to write update cache")


def is_cache_fresh(cache: Dict[str, Any], freshness_seconds: int = ONE_DAY_SECONDS) -> bool:
    try:
        last_checked = float(cache.get("last_checked", 0.0))
        return (time.time() - last_checked) < max(0, int(freshness_seconds))
    except Exception:
        return False


def fetch_update_json(url: str, timeout: float = 4.0) -> Dict[str, Any]:
    import urllib.request

    with urllib.request.urlopen(url, timeout=timeout) as resp:  # nosec - controlled URL
        content_type = resp.headers.get("Content-Type", "").lower()
        raw = resp.read().decode("utf-8")
        data = json.loads(raw)
    # Normalize
    result = {
        "version": str(data.get("version", "")),
        "changelog": str(data.get("changelog", "")),
        "url": str(data.get("url", "")),
    }
    if "hash" in data:
        result["hash"] = str(data.get("hash"))
    return result


def is_newer_version(current: str, remote: str, include_prereleases: bool = False) -> bool:
    try:
        cur = Version(current)
        rem = Version(remote)
        if not include_prereleases and rem.is_prerelease:
            return False
        return rem > cur
    except Exception:
        return False


@dataclass
class UpdateChecker:
    url: str = DEFAULT_UPDATE_URL
    freshness_seconds: int = ONE_DAY_SECONDS
    timeout: float = 4.0
    include_prereleases: bool = False

    _timer: Optional[threading.Timer] = None
    _on_update: Optional[Callable[[str, str, str], None]] = None

    def set_on_update(self, callback: Callable[[str, str, str], None]) -> None:
        self._on_update = callback

    def cancel(self) -> None:
        try:
            if self._timer is not None:
                self._timer.cancel()
        except Exception:
            pass
        finally:
            self._timer = None

    def schedule(self, delay_seconds: float = 5.0) -> None:
        self.cancel()
        self._timer = threading.Timer(max(0.0, float(delay_seconds)), self._maybe_check)
        self._timer.daemon = True
        self._timer.start()

    def check_now(self, force: bool = False) -> Optional[Dict[str, Any]]:
        cache = read_cache()
        if not force and is_cache_fresh(cache, self.freshness_seconds):
            logger.info("Update check skipped: cache fresh")
            return cache.get("last_result")
        try:
            result = fetch_update_json(self.url, timeout=self.timeout)
        except Exception:
            logger.exception("Update check failed")
            return None
        finally:
            # Always record the attempt time
            cache = {"last_checked": time.time(), "last_result": cache.get("last_result")}

        # If newer, notify and store result
        remote_version = result.get("version", "")
        if is_newer_version(APP_VERSION, remote_version, self.include_prereleases):
            cache["last_result"] = result
            if self._on_update is not None:
                try:
                    self._on_update(remote_version, result.get("changelog", ""), result.get("url", ""))
                except Exception:
                    logger.exception("on_update callback failed")

        write_cache(cache)
        return cache.get("last_result")

    # Internal
    def _maybe_check(self) -> None:
        try:
            self.check_now(force=False)
        except Exception:
            logger.exception("Scheduled update check failed")


__all__ = [
    "DEFAULT_UPDATE_URL",
    "get_cache_path",
    "read_cache",
    "write_cache",
    "is_cache_fresh",
    "fetch_update_json",
    "is_newer_version",
    "UpdateChecker",
]


