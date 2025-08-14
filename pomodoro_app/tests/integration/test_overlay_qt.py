from __future__ import annotations

import typing as _t

import pytest

from pomodoro_app.adapters.notifications.overlay import QtOverlay


@pytest.mark.qt_log_ignore(".*")
def test_overlay_show_message(qtbot: _t.Any) -> None:  # type: ignore[override]
    overlay = QtOverlay(duration_ms=100)
    overlay.enabled = True
    qtbot.addWidget(overlay)
    overlay.show_message("Title", "Message")
    assert overlay.isVisible()
    qtbot.waitUntil(lambda: not overlay.isVisible(), timeout=2000)


