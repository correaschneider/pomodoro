from __future__ import annotations

from pathlib import Path

from pomodoro_app.plugin_manager.manager import create_plugin_manager, load_and_register_plugins, wire_timer_service
from pomodoro_app.core.timer_service import TimerService


def test_wire_timer_service_invokes_hooks(tmp_path: Path) -> None:
    base = tmp_path / "plugins"
    base.mkdir()
    plug = base / "wired"
    plug.mkdir()
    (plug / "main.py").write_text(
        """
from pomodoro_app.plugin_manager.spec import hookimpl

CALLED = {"tick": 0, "end": 0}

@hookimpl
def on_timer_tick(elapsed, remaining, state):
    CALLED["tick"] += 1

@hookimpl
def on_cycle_end(session):
    CALLED["end"] += 1
""",
        encoding="utf-8",
    )
    (plug / "plugin.toml").write_text(
        """
[plugin]
name = "wired"
version = "0.1.0"
compatible_with = ">=0.1.0"
""",
        encoding="utf-8",
    )

    pm = create_plugin_manager()
    load_and_register_plugins(pm, base)

    svc = TimerService(tick_interval=0.01)
    unsub = wire_timer_service(pm, svc)
    try:
        svc.start_focus(dur_s=1)
    finally:
        svc.stop()
        unsub()

    # Load the plugin module namespace to verify counters
    import importlib

    mod = importlib.import_module("plugin_wired")
    assert mod.CALLED["tick"] >= 1
    assert mod.CALLED["end"] == 1


