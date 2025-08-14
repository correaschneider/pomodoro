from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.adapters.notifications")


class NotificationBackend:
    def send(self, title: str, message: str, actions: Optional[Iterable[tuple[str, Any]]] = None, urgency: str = "normal") -> None:  # noqa: D401
        """Send a notification. Implemented by platform backends."""
        raise NotImplementedError


@dataclass
class OverlayAdapter:
    enabled: bool = False

    def show_message(self, title: str, message: str) -> None:
        logger.info("Overlay: %s - %s", title, message)


class NotificationService:
    def __init__(self, tray: Any | None = None, overlay: OverlayAdapter | None = None) -> None:
        self._backend: NotificationBackend | None = None
        self._tray = tray
        self._overlay = overlay or OverlayAdapter(enabled=False)

    # Backend selection to be implemented in later subtasks
    def choose_backend(self) -> None:
        # Try platform-specific backends by import
        try:
            from .linux_notify import LinuxNotify2Backend  # type: ignore

            self._backend = LinuxNotify2Backend()
            return
        except Exception:
            pass
        try:
            from .windows_toast import WinToastBackend  # type: ignore

            self._backend = WinToastBackend()
            return
        except Exception:
            pass
        try:
            from .macos_notify import MacPyncBackend, MacOsascriptBackend  # type: ignore

            try:
                self._backend = MacPyncBackend()
                return
            except Exception:
                self._backend = MacOsascriptBackend()
                return
        except Exception:
            pass
        self._backend = None

    def notify(self, title: str, message: str, actions: Optional[Iterable[tuple[str, Any]]] = None, urgency: str = "normal") -> None:
        # Try backend first
        if self._backend:
            try:
                self._backend.send(title, message, actions, urgency)
                return
            except Exception:
                logger.exception("backend notification failed; falling back")
                self._backend = None

        # Overlay fallback
        if self._overlay and self._overlay.enabled:
            try:
                self._overlay.show_message(title, message)
                return
            except Exception:
                logger.exception("overlay notification failed; falling back")

        # Tray fallback
        if self._tray is not None:
            try:
                self._tray.showMessage(title, message)
                return
            except Exception:
                logger.exception("tray notification failed; logging only")

        # Final fallback: log
        logger.info("Notification: %s - %s", title, message)

    # Convenience hooks for domain events
    def on_cycle_start(self, title: str = "Pomodoro", message: str = "Focus started") -> None:
        self.notify(title, message)

    def on_cycle_end(self, title: str = "Pomodoro", message: str = "Cycle finished") -> None:
        self.notify(title, message)


__all__ = ["NotificationBackend", "OverlayAdapter", "NotificationService"]


def wire_timer_notifications(service: Any, notifier: NotificationService) -> Any:
    """Subscribe to TimerService events and send notifications.

    Returns an unsubscribe callable.
    """

    def _on_cycle_end(session: Any) -> None:  # noqa: ARG001
        try:
            notifier.on_cycle_end()
        except Exception:
            logger.exception("failed to send cycle_end notification")

    unsub_end = service.on_cycle_end(_on_cycle_end)

    def _unsubscribe() -> None:
        try:
            unsub_end()
        except Exception:
            pass

    return _unsubscribe


