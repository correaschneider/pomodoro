from __future__ import annotations

import math

from pomodoro_app.adapters.gui.time_utils import format_mm_ss


def test_format_mm_ss_basic_cases() -> None:
    assert format_mm_ss(0) == "00:00"
    assert format_mm_ss(5) == "00:05"
    assert format_mm_ss(65) == "01:05"
    assert format_mm_ss(600) == "10:00"


def test_format_mm_ss_negative_and_float_inputs() -> None:
    assert format_mm_ss(-10) == "00:00"
    assert format_mm_ss(59.9) == "00:59"
    assert format_mm_ss(60.1) == "01:00"
    # large float
    assert format_mm_ss(3_600.5) == "60:00"


def test_format_mm_ss_non_numeric() -> None:
    assert format_mm_ss("abc") == "00:00"  # type: ignore[arg-type]


