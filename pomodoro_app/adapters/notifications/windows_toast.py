from __future__ import annotations

from typing import Any, Iterable, Optional

from pomodoro_app.infrastructure.logging import get_logger
from .service import NotificationBackend


logger = get_logger("pomodoro.adapters.notifications.windows")


class WinToastBackend(NotificationBackend):
    """win10toast backend wrapper for Windows.

    Safe to import even when win10toast is not available; errors surface on send().
    """

    def __init__(self, app_name: str = "Pomodoro") -> None:
        self._app_name = app_name

    def send(
        self,
        title: str,
        message: str,
        actions: Optional[Iterable[tuple[str, Any]]] = None,
        urgency: str = "normal",
    ) -> None:
        try:
            from win10toast import ToastNotifier  # type: ignore

            toaster = ToastNotifier()
            toast_duration = 5 if urgency == "normal" else 10
            toaster.show_toast(title, message, duration=toast_duration, threaded=True)
        except Exception:
            logger.exception("win10toast failed")
            raise


__all__ = ["WinToastBackend"]


