from __future__ import annotations

from datetime import datetime, timedelta

from pomodoro_app.core.models import Session, SessionType, TimerState
from pomodoro_app.infrastructure.db.connection import connect
from pomodoro_app.infrastructure.db.schema import ensure_schema
from pomodoro_app.infrastructure.db.repositories import SessionRepository
from pomodoro_app.infrastructure.db.stats import StatsService


def _mk_session(id_offset: int, start: datetime, duration: int, ended_early: bool, s_type: SessionType) -> Session:
    uuid = __import__("uuid").uuid5(__import__("uuid").NAMESPACE_DNS, f"sess-{id_offset}")
    ended_at = start + timedelta(seconds=(duration - 10 if ended_early else duration))
    return Session(
        id=uuid,
        type=s_type,
        duration_s=duration,
        started_at=start,
        ended_at=ended_at,
        state=TimerState.IDLE,
    )


def test_stats_compute(temp_conn) -> None:
    conn = temp_conn
    repo = SessionRepository(conn)
    stats = StatsService(conn)

    base = datetime(2024, 1, 1, 12, 0, 0)
    repo.add(_mk_session(1, base, 1500, False, SessionType.FOCUS))  # full focus 25m
    repo.add(_mk_session(2, base + timedelta(minutes=30), 300, True, SessionType.BREAK))  # early break
    repo.add(_mk_session(3, base + timedelta(hours=1), 1500, True, SessionType.FOCUS))  # early focus

    res = stats.compute()
    assert res.total_focus_seconds == 3000
    assert res.total_break_seconds == 300
    assert res.sessions_count == 3
    assert res.interruptions == 2


