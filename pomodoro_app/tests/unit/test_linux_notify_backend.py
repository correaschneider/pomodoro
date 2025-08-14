from __future__ import annotations

import types

import pytest

from pomodoro_app.adapters.notifications.linux_notify import LinuxNotify2Backend


def test_linux_notify2_backend_import_error(monkeypatch: object) -> None:
    # Simulate notify2 import error
    monkeypatch.setitem(__import__("sys").modules, "notify2", None)
    backend = LinuxNotify2Backend()
    with pytest.raises(Exception):
        backend.send("T", "M")


