from __future__ import annotations

import threading
from datetime import datetime, timedelta

from pomodoro_app.core.models import Session, SessionType, TimerState
from pomodoro_app.infrastructure.db.repositories import SessionRepository


def _mk_session(idx: int, base: datetime) -> Session:
    return Session(
        id=__import__("uuid").uuid4(),
        type=SessionType.FOCUS,
        duration_s=60,
        started_at=base + timedelta(seconds=idx),
        ended_at=base + timedelta(seconds=idx + 60),
        state=TimerState.IDLE,
    )


def test_concurrent_inserts_serialized_by_sqlite(temp_conn) -> None:
    conn = temp_conn
    repo = SessionRepository(conn)
    base = datetime(2024, 1, 1, 0, 0, 0)

    def worker(offset: int) -> None:
        for j in range(10):
            repo.add(_mk_session(offset * 100 + j, base))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Expect 40 sessions total
    assert len(repo.last_n(1000)) == 40

