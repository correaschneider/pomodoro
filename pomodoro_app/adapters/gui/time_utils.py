from __future__ import annotations


def format_mm_ss(total_seconds: int | float) -> str:
    """Format seconds into mm:ss string, clamping negatives to 00:00.

    Non-integer values are floored to the nearest lower integer before formatting.
    """

    try:
        seconds_int = int(total_seconds)
    except Exception:
        seconds_int = 0

    if seconds_int < 0:
        seconds_int = 0

    minutes = seconds_int // 60
    seconds = seconds_int % 60
    return f"{minutes:02d}:{seconds:02d}"


__all__ = ["format_mm_ss"]


