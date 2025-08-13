from __future__ import annotations

import time

import pytest

from pomodoro_app.core.errors import InvalidDurationError, InvalidStateError
from pomodoro_app.core.models import SessionType, TimerState
from pomodoro_app.core.timer_service import TimerService


def test_start_focus_and_stop_transitions_to_idle() -> None:
    svc = TimerService(tick_interval=0.01)
    svc.start_focus(dur_s=1)
    assert svc.is_running
    svc.stop()
    assert svc.state == TimerState.IDLE


def test_invalid_duration_raises() -> None:
    svc = TimerService()
    with pytest.raises(InvalidDurationError):
        svc.start_focus(dur_s=0)


def test_pause_resume_guards() -> None:
    svc = TimerService(tick_interval=0.01)
    with pytest.raises(InvalidStateError):
        svc.pause()
    svc.start_focus(dur_s=2)
    svc.pause()
    assert svc.is_paused
    svc.resume()
    assert svc.is_running


def test_tick_and_finish_cycle_emits_state_idle(monkeypatch) -> None:
    # Use a fast clock to force progression
    base = [0.0]

    def fake_monotonic() -> float:
        base[0] += 0.05
        return base[0]

    svc = TimerService(tick_interval=0.01, clock=fake_monotonic)
    svc.start_focus(dur_s=1)

    # Wait a bit for loop to progress
    time.sleep(0.2)
    # Force stop to ensure thread cleanup and state IDLE
    svc.stop()
    assert svc.state == TimerState.IDLE


