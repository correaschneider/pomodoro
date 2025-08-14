from __future__ import annotations

from typing import Callable

from pomodoro_app.infrastructure.logging import get_logger
from pomodoro_app.adapters.notifications.service import NotificationService
from pomodoro_app.infrastructure.update.checker import UpdateChecker


logger = get_logger("pomodoro.infrastructure.update")


def wire_update_ui(main_window: "object", checker: UpdateChecker, notifier: NotificationService) -> Callable[[], None]:
    """Wire UpdateChecker to the MainWindow UI and notifications.

    - Connects the 'Check for updates' menu action to checker.check_now(force=True)
    - On update available, sends a notification via NotificationService

    Returns an unsubscribe callable to remove connections.
    """

    # Install callback: route to notifier
    def _on_update(version: str, changelog: str, url: str) -> None:
        try:
            title = f"Update available: {version}"
            message = changelog or url or ""
            notifier.notify(title, message)
        except Exception:
            logger.exception("failed to notify about update")

    checker.set_on_update(_on_update)

    # Connect UI action to force check
    try:
        action = getattr(main_window, "checkUpdatesAction")
        action.triggered.connect(lambda: checker.check_now(force=True))  # type: ignore[attr-defined]
    except Exception:
        logger.exception("failed to wire Check for updates action")

    def _unsubscribe() -> None:
        try:
            checker.set_on_update(lambda *_: None)
        except Exception:
            pass

    return _unsubscribe


__all__ = ["wire_update_ui"]


