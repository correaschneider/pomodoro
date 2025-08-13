from __future__ import annotations

from datetime import datetime, timedelta

from pomodoro_app.core.models import Session, SessionType, TimerState
from pomodoro_app.infrastructure.db.connection import connect
from pomodoro_app.infrastructure.db.schema import ensure_schema
from pomodoro_app.infrastructure.db.repositories import SessionRepository


def _mk_session(base: datetime, idx: int) -> Session:
    return Session(
        id=__import__("uuid").uuid4(),
        type=SessionType.FOCUS if idx % 2 == 0 else SessionType.BREAK,
        duration_s=60,
        started_at=base + timedelta(minutes=idx),
        ended_at=base + timedelta(minutes=idx, seconds=60),
        state=TimerState.IDLE,
    )


def test_add_and_last_n_and_period() -> None:
    conn = connect()
    ensure_schema(conn)
    repo = SessionRepository(conn)

    base = datetime(2024, 1, 1, 12, 0, 0)
    sessions = [_mk_session(base, i) for i in range(5)]
    for s in sessions:
        repo.add(s)

    # last_n
    assert [s.id for s in repo.last_n(2)] == [sessions[3].id, sessions[4].id]

    # list_by_period
    window_start = base + timedelta(minutes=1)
    window_end = base + timedelta(minutes=3)
    by_period = repo.list_by_period(window_start, window_end)
    assert [s.id for s in by_period] == [sessions[1].id, sessions[2].id, sessions[3].id]


