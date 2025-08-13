from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any, Iterable, Sequence
from uuid import UUID

from pomodoro_app.core.models import Session, SessionType, TimerState
from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.infrastructure.db")


def _dt_to_str(dt: datetime | None) -> str | None:
    return dt.isoformat() if dt is not None else None


def _str_to_dt(val: str | None) -> datetime | None:
    return datetime.fromisoformat(val) if val is not None else None


class SessionRepository:
    """Repository for persisting and querying `Session` records."""

    def __init__(self, conn: sqlite3.Connection) -> None:
        self._conn = conn

    # --- Commands ------------------------------------------------------------
    def add(self, session: Session) -> None:
        """Insert a session into the database.

        Idempotency is not guaranteed; caller is responsible for unique IDs.
        """

        logger.info("Inserting session %s (%s)", session.id, session.type.name)
        self._conn.execute(
            """
            INSERT INTO sessions(id, type, duration_s, started_at, ended_at, state)
            VALUES(?, ?, ?, ?, ?, ?)
            """,
            (
                str(session.id),
                session.type.name,
                int(session.duration_s),
                _dt_to_str(session.started_at),
                _dt_to_str(session.ended_at),
                session.state.name,
            ),
        )
        # autocommit is enabled by connection factory; keep explicit commit for clarity
        try:
            self._conn.commit()
        except Exception:
            logger.exception("Commit failed after session insert")
            raise

    # --- Queries -------------------------------------------------------------
    def list_by_period(self, start: datetime | None, end: datetime | None) -> list[Session]:
        """List sessions whose `started_at` falls within [start, end].

        If `start` or `end` are None, the bound is open on that side.
        Results are ordered by `started_at` ascending.
        """

        clauses: list[str] = []
        params: list[Any] = []
        if start is not None:
            clauses.append("started_at >= ?")
            params.append(_dt_to_str(start))
        if end is not None:
            clauses.append("started_at <= ?")
            params.append(_dt_to_str(end))

        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"SELECT id, type, duration_s, started_at, ended_at, state FROM sessions{where} ORDER BY started_at ASC"

        rows = self._conn.execute(sql, params).fetchall()
        return [self._row_to_session(row) for row in rows]

    def last_n(self, n: int) -> list[Session]:
        """Return the last `n` sessions ordered by `started_at` descending."""

        rows = self._conn.execute(
            """
            SELECT id, type, duration_s, started_at, ended_at, state
            FROM sessions
            ORDER BY started_at DESC
            LIMIT ?
            """,
            (int(max(0, n)),),
        ).fetchall()
        sessions = [self._row_to_session(row) for row in rows]
        sessions.reverse()  # return ascending chronological order
        return sessions

    # --- Mapping -------------------------------------------------------------
    @staticmethod
    def _row_to_session(row: Sequence[Any]) -> Session:
        sid, stype, duration_s, started_at, ended_at, state = row
        return Session(
            id=UUID(str(sid)),
            type=SessionType[str(stype)],
            duration_s=int(duration_s),
            started_at=_str_to_dt(started_at),
            ended_at=_str_to_dt(ended_at),
            state=TimerState[str(state)],
        )


__all__ = ["SessionRepository"]


