from __future__ import annotations

from typing import Any, Iterable, Optional

from pomodoro_app.infrastructure.logging import get_logger
from .service import NotificationBackend


logger = get_logger("pomodoro.adapters.notifications.linux")


class LinuxNotify2Backend(NotificationBackend):
    """notify2 (DBus) backend wrapper for Linux desktops.

    Safe to import even when notify2 is not available; errors surface on send().
    """

    _initialized: bool = False

    def __init__(self, app_name: str = "pomodoro_app") -> None:
        self._app_name = app_name

    def _ensure_init(self) -> Any:
        try:
            import notify2  # type: ignore

            if not LinuxNotify2Backend._initialized:
                try:
                    notify2.init(self._app_name)
                    LinuxNotify2Backend._initialized = True
                except Exception:
                    logger.exception("notify2.init failed")
                    raise
            return notify2
        except Exception as exc:
            logger.exception("notify2 import/init failed: %s", exc)
            raise

    def send(
        self,
        title: str,
        message: str,
        actions: Optional[Iterable[tuple[str, Any]]] = None,
        urgency: str = "normal",
    ) -> None:
        notify2 = self._ensure_init()
        try:
            n = notify2.Notification(title, message)
            # Map urgency when available
            try:
                urgency_map = {
                    "low": getattr(notify2, "URGENCY_LOW", 0),
                    "normal": getattr(notify2, "URGENCY_NORMAL", 1),
                    "critical": getattr(notify2, "URGENCY_CRITICAL", 2),
                }
                n.set_urgency(urgency_map.get(urgency, urgency_map["normal"]))
            except Exception:
                pass
            n.show()
        except Exception:
            logger.exception("notify2 Notification failed")
            raise


__all__ = ["LinuxNotify2Backend"]


