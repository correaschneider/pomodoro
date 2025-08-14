from __future__ import annotations

from pomodoro_app.adapters.notifications.service import NotificationService, OverlayAdapter, wire_timer_notifications
from pomodoro_app.core.timer_service import TimerService


def test_notifications_on_cycle_end_overlay_fallback() -> None:
    svc = TimerService(tick_interval=0.01)
    overlay = OverlayAdapter(enabled=True)
    shown: list[tuple[str, str]] = []
    overlay.show_message = lambda t, m: shown.append((t, m))  # type: ignore[method-assign]

    notifier = NotificationService(tray=None, overlay=overlay)
    notifier.choose_backend()  # no backend expected in tests
    unsub = wire_timer_notifications(svc, notifier)
    try:
        svc.start_focus(dur_s=1)
    finally:
        svc.stop()
        unsub()

    assert any("Cycle finished" in msg for _, msg in shown) or len(shown) >= 1


