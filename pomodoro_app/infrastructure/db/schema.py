from __future__ import annotations

import sqlite3
from typing import Iterable

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.infrastructure.db")


SCHEMA_STATEMENTS: tuple[str, ...] = (
    # Sessions: stores historical timer sessions
    """
    CREATE TABLE IF NOT EXISTS sessions (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        duration_s INTEGER NOT NULL,
        started_at TEXT,
        ended_at TEXT,
        state TEXT NOT NULL
    );
    """,
    # Settings: simple key/value store (JSON-encoded values at repository layer)
    """
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    );
    """,
    # Optional indices to speed common queries
    """
    CREATE INDEX IF NOT EXISTS idx_sessions_started_at ON sessions(started_at);
    """,
)


def _execute_many(conn: sqlite3.Connection, statements: Iterable[str]) -> None:
    cursor = conn.cursor()
    try:
        for stmt in statements:
            cursor.execute(stmt)
        conn.commit()
    finally:
        cursor.close()


def ensure_schema(conn: sqlite3.Connection) -> None:
    """Create the database schema if it does not already exist.

    Idempotent. Safe to call multiple times at startup.
    """
    try:
        _execute_many(conn, SCHEMA_STATEMENTS)
        logger.info("SQLite schema ensured (sessions, settings)")
    except Exception:
        logger.exception("Failed to ensure SQLite schema")
        raise


__all__ = ["ensure_schema", "SCHEMA_STATEMENTS"]


