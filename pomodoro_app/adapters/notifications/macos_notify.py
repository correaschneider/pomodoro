from __future__ import annotations

import subprocess
from typing import Any, Iterable, Optional

from pomodoro_app.infrastructure.logging import get_logger
from .service import NotificationBackend


logger = get_logger("pomodoro.adapters.notifications.macos")


class MacPyncBackend(NotificationBackend):
    def send(
        self,
        title: str,
        message: str,
        actions: Optional[Iterable[tuple[str, Any]]] = None,
        urgency: str = "normal",
    ) -> None:
        try:
            import pync  # type: ignore

            pync.Notifier.notify(message, title=title)
        except Exception:
            logger.exception("pync failed")
            raise


class MacOsascriptBackend(NotificationBackend):
    def send(
        self,
        title: str,
        message: str,
        actions: Optional[Iterable[tuple[str, Any]]] = None,
        urgency: str = "normal",
    ) -> None:
        try:
            script = f'display notification "{message}" with title "{title}"'
            subprocess.run(["osascript", "-e", script], check=True)
        except Exception:
            logger.exception("osascript failed")
            raise


__all__ = ["MacPyncBackend", "MacOsascriptBackend"]


