from __future__ import annotations

from types import SimpleNamespace

from pomodoro_app.infrastructure.update.checker import UpdateChecker
from pomodoro_app.adapters.notifications.service import NotificationService, OverlayAdapter
from pomodoro_app.infrastructure.update.integration import wire_update_ui


def test_wire_update_ui_sends_notification_on_update() -> None:
    checker = UpdateChecker(url="http://127.0.0.1:9/invalid", freshness_seconds=0)
    overlay = OverlayAdapter(enabled=True)
    shown: list[tuple[str, str]] = []
    overlay.show_message = lambda t, m: shown.append((t, m))  # type: ignore[method-assign]
    notifier = NotificationService(tray=None, overlay=overlay)

    mw = SimpleNamespace(checkUpdatesAction=SimpleNamespace(triggered=SimpleNamespace(connect=lambda f: None)))
    unsub = wire_update_ui(mw, checker, notifier)
    try:
        if checker._on_update:  # type: ignore[attr-defined]
            checker._on_update("9.9.9", "Changelog", "https://example.com")
    finally:
        unsub()

    assert any("Update available" in t for t, _ in shown)


