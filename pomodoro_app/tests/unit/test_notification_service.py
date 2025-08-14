from __future__ import annotations

from types import SimpleNamespace

from pomodoro_app.adapters.notifications.service import NotificationService, OverlayAdapter, NotificationBackend


class DummyBackend(NotificationBackend):
    def __init__(self) -> None:
        self.sent: list[tuple[str, str]] = []

    def send(self, title: str, message: str, actions=None, urgency: str = "normal") -> None:  # noqa: D401
        self.sent.append((title, message))


def test_notify_uses_backend_first() -> None:
    svc = NotificationService()
    backend = DummyBackend()
    svc._backend = backend  # type: ignore[attr-defined]
    svc.notify("T", "M")
    assert backend.sent == [("T", "M")]


def test_notify_falls_back_to_overlay_then_tray() -> None:
    overlay = OverlayAdapter(enabled=True)
    shown: list[tuple[str, str]] = []
    overlay.show_message = lambda t, m: shown.append((t, m))  # type: ignore[method-assign]

    tray = SimpleNamespace()
    tray_calls: list[tuple[str, str]] = []
    tray.showMessage = lambda t, m: tray_calls.append((t, m))  # type: ignore[attr-defined]

    svc = NotificationService(tray=tray, overlay=overlay)
    svc.notify("A", "B")

    assert shown == [("A", "B")]  # overlay used
    assert tray_calls == []  # not needed


