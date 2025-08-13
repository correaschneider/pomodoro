from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from typing import Any, Iterable, Iterator

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.infrastructure.db")


def safe_execute(conn: sqlite3.Connection, sql: str, params: Iterable[Any] | None = None) -> sqlite3.Cursor:
    """Execute SQL with basic error logging and re-raise on failure."""
    try:
        return conn.execute(sql, tuple(params or ()))
    except Exception:
        logger.exception("DB execute failed: %s | params=%s", sql.strip().splitlines()[0], params)
        raise


def safe_executemany(conn: sqlite3.Connection, sql: str, seq_of_params: Iterable[Iterable[Any]]) -> sqlite3.Cursor:
    try:
        return conn.executemany(sql, seq_of_params)
    except Exception:
        logger.exception("DB executemany failed: %s", sql.strip().splitlines()[0])
        raise


@contextmanager
def transaction(conn: sqlite3.Connection) -> Iterator[None]:
    """Context manager for an explicit transaction with logging.

    Works even when isolation_level=None by issuing BEGIN/COMMIT/ROLLBACK.
    """
    try:
        conn.execute("BEGIN")
        yield
        conn.execute("COMMIT")
    except Exception:
        try:
            conn.execute("ROLLBACK")
        except Exception:
            logger.exception("DB rollback failed")
        logger.exception("DB transaction failed")
        raise


__all__ = ["safe_execute", "safe_executemany", "transaction"]


