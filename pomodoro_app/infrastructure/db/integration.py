from __future__ import annotations

import sqlite3
from typing import Any, Callable, Dict

from pomodoro_app.core.models import Session
from pomodoro_app.core.timer_service import TimerService
from pomodoro_app.infrastructure.logging import get_logger

from .repositories import SessionRepository, SettingsRepository


logger = get_logger("pomodoro.infrastructure.db")


def wire_persistence(service: TimerService, conn: sqlite3.Connection) -> Callable[[], None]:
    """Subscribe to domain events and persist data accordingly.

    - On cycle_end: persist the finished `Session`.

    Returns an unsubscribe callable.
    """

    repo = SessionRepository(conn)

    def on_cycle_end(session: Session) -> None:
        try:
            repo.add(session)
            logger.info("Persisted finished session %s", session.id)
        except Exception:
            logger.exception("Failed to persist finished session")

    unsub = service.on_cycle_end(on_cycle_end)
    logger.info("Persistence wiring subscribed to TimerService.cycle_end")

    def unsubscribe() -> None:
        try:
            unsub()
        finally:
            logger.info("Persistence wiring unsubscribed from TimerService.cycle_end")

    return unsubscribe


def load_settings(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Load application settings with safe defaults.

    Returns a dictionary with keys: durations, overlay, language.
    """

    repo = SettingsRepository(conn)
    durations = repo.get("durations", {"focus": 25 * 60, "break": 5 * 60})
    overlay = repo.get("overlay", False)
    language = repo.get("language", "system")
    logger.info("Loaded settings: language=%s overlay=%s", language, overlay)
    return {
        "durations": durations,
        "overlay": overlay,
        "language": language,
    }


__all__ = ["wire_persistence", "load_settings"]


