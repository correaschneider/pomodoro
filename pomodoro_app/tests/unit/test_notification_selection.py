from __future__ import annotations

import types

from pomodoro_app.adapters.notifications.service import NotificationService


def test_choose_backend_handles_missing_imports(monkeypatch: object) -> None:
    # Force imports to fail
    monkeypatch.setitem(__import__("sys").modules, "pomodoro_app.adapters.notifications.linux_notify", None)
    monkeypatch.setitem(__import__("sys").modules, "pomodoro_app.adapters.notifications.windows_toast", None)
    monkeypatch.setitem(__import__("sys").modules, "pomodoro_app.adapters.notifications.macos_notify", None)

    svc = NotificationService()
    svc.choose_backend()
    assert svc._backend is None  # type: ignore[attr-defined]


