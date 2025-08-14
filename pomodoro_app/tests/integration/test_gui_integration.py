from __future__ import annotations

import typing as _t

import pytest

from pomodoro_app.adapters.gui.bridge import GuiBridge
from pomodoro_app.adapters.gui.controller import GuiController
from pomodoro_app.adapters.gui.main_window import MainWindow
from pomodoro_app.adapters.system_tray import TrayController
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


@pytest.mark.qt_log_ignore(".*")
def test_tray_controller_menu_and_tooltip(qtbot: _t.Any) -> None:  # type: ignore[override]
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()

    service = TimerService(tick_interval=0.01)
    bridge = GuiBridge()

    tray = TrayController(parent=window, service=service, main_window=window, bridge=bridge)

    # Start a short session to drive tooltip updates
    service.start_focus(dur_s=1)
    qtbot.waitUntil(lambda: tray.toolTip() != "Pomodoro", timeout=1500)

    # Expect actions to be wired (enabled/disabled will vary by state)
    assert tray.act_start_focus is not None
    assert tray.act_pause is not None
    assert tray.act_resume is not None
    assert tray.act_stop is not None

    # Cleanup
    service.stop()


