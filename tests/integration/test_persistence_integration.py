from __future__ import annotations

import time
from datetime import datetime, timedelta

from pomodoro_app.core.timer_service import TimerService
from pomodoro_app.infrastructure.db.integration import load_settings, wire_persistence
from pomodoro_app.infrastructure.db.repositories import SessionRepository, SettingsRepository


def test_wire_persistence_persists_finished_sessions(temp_conn) -> None:
    conn = temp_conn
    repo = SessionRepository(conn)

    # Use small tick for speed
    service = TimerService(tick_interval=0.01)
    unsubscribe = wire_persistence(service, conn)
    try:
        service.start_focus(dur_s=1)

        # Wait until a session is persisted (within 2 seconds)
        deadline = time.time() + 2.0
        while time.time() < deadline and len(repo.last_n(1)) < 1:
            time.sleep(0.02)

        assert len(repo.last_n(1)) == 1
    finally:
        service.stop()
        unsubscribe()


def test_load_settings_defaults_and_overrides(temp_conn) -> None:
    conn = temp_conn
    repo = SettingsRepository(conn)

    defaults = load_settings(conn)
    assert defaults["durations"]["focus"] == 25 * 60
    assert defaults["durations"]["break"] == 5 * 60
    assert defaults["overlay"] is False
    assert defaults["language"] == "system"

    repo.set("durations", {"focus": 10, "break": 20})
    repo.set("overlay", True)
    repo.set("language", "en")

    loaded = load_settings(conn)
    assert loaded == {"durations": {"focus": 10, "break": 20}, "overlay": True, "language": "en"}

