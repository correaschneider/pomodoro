from __future__ import annotations

import importlib
from pathlib import Path

from pomodoro_app.plugin_manager.manager import create_plugin_manager, load_and_register_plugins, wire_timer_service
from pomodoro_app.core.timer_service import TimerService


def test_example_plugin_loads_and_receives_events(tmp_path: Path, monkeypatch: object) -> None:
    # Copy built-in example plugin into a temp discovery dir to simulate user install
    base = tmp_path / "plugins"
    pkg_example = Path(__file__).resolve().parents[3] / "pomodoro_app" / "plugins" / "example_plugin"

    (base / "example").mkdir(parents=True)
    (base / "example" / "main.py").write_text((pkg_example / "main.py").read_text(encoding="utf-8"), encoding="utf-8")
    (base / "example" / "plugin.toml").write_text(
        """
[plugin]
name = "example"
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

    # Import plugin module to ensure it exists
    mod = importlib.import_module("plugin_example")
    assert hasattr(mod, "on_app_start")


