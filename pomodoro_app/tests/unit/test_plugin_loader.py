from __future__ import annotations

from pathlib import Path

from pomodoro_app.plugin_manager.manager import create_plugin_manager, load_and_register_plugins


def test_load_and_register_plugins_success(tmp_path: Path) -> None:
    base = tmp_path / "plugins"
    base.mkdir()
    plug = base / "demo"
    plug.mkdir()
    (plug / "main.py").write_text(
        """
from pomodoro_app.plugin_manager.spec import hookimpl

@hookimpl
def on_app_start(app_ctx):
    pass
""",
        encoding="utf-8",
    )
    (plug / "plugin.toml").write_text(
        """
[plugin]
name = "demo"
version = "0.1.0"
compatible_with = ">=0.1.0"

[access]
filesystem = false
network = false
requires_gui = false
""",
        encoding="utf-8",
    )

    pm = create_plugin_manager()
    loaded, skipped = load_and_register_plugins(pm, base)
    assert loaded == 1 and skipped == 0


