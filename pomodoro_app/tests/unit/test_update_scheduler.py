from __future__ import annotations

import time

from pomodoro_app.infrastructure.update.checker import UpdateChecker


def test_schedule_and_cancel() -> None:
    uc = UpdateChecker(url="http://127.0.0.1:9/invalid", freshness_seconds=0)
    called: list[tuple[str, str, str]] = []
    uc.set_on_update(lambda v, c, u: called.append((v, c, u)))
    uc.schedule(delay_seconds=0.05)
    time.sleep(0.1)
    uc.cancel()
    # No crash and timer cleaned
    assert uc._timer is None  # type: ignore[attr-defined]


