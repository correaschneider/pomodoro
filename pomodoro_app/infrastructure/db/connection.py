from __future__ import annotations

import sqlite3
from pathlib import Path

from platformdirs import user_data_dir

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.infrastructure.db")


def _ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def get_db_path(app_name: str = "pomodoro_app") -> Path:
    """Return the absolute path to the SQLite database file in user data dir.

    The file will be located under the application data directory inside a
    "db" subfolder, e.g.: <user_data_dir>/<app_name>/db/pomodoro.sqlite3
    """

    base = Path(user_data_dir(app_name)) / "db"
    _ensure_directory(base)
    return base / "pomodoro.sqlite3"


def connect(db_path: Path | None = None) -> sqlite3.Connection:
    """Create a SQLite connection with WAL and sensible pragmas applied.

    - check_same_thread=False to allow usage from controller/threads with care
    - isolation_level=None (autocommit) and explicit transactions if needed
    - PRAGMA journal_mode=WAL and foreign_keys=ON
    """

    path = Path(db_path) if db_path else get_db_path()
    _ensure_directory(path.parent)

    logger.info("Opening SQLite database at %s", path)
    conn = sqlite3.connect(str(path), check_same_thread=False, isolation_level=None)
    # Apply recommended pragmas
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute("PRAGMA synchronous=NORMAL;")
    except Exception:
        logger.exception("Failed to apply SQLite PRAGMAs")
    return conn


__all__ = ["get_db_path", "connect"]


