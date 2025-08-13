from __future__ import annotations

import typing as _t

import pytest

from pomodoro_app.adapters.gui.bridge import GuiBridge
from pomodoro_app.adapters.gui.controller import GuiController
from pomodoro_app.adapters.gui.main_window import MainWindow
from pomodoro_app.core.timer_service import TimerService


@pytest.mark.qt_log_ignore(".*")
def test_controller_wiring_emits_tick_and_updates_label(qtbot: _t.Any) -> None:  # type: ignore[override]
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    service = TimerService(tick_interval=0.01)
    bridge = GuiBridge()
    controller = GuiController(window, service, bridge)

    # Start a short session and wait for at least one tick
    service.start_focus(dur_s=1)

    ticks: list[tuple[int, int, object]] = []
    bridge.tick.connect(lambda e, r, s: ticks.append((e, r, s)))

    qtbot.waitUntil(lambda: len(ticks) > 0, timeout=1500)

    # Label should have updated away from initial 00:00
    assert window.timerLabel.text() != "00:00"

    # Cleanup
    service.stop()
    controller.dispose()


