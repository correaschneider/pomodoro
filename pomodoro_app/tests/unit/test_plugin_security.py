from __future__ import annotations

from pathlib import Path

from pomodoro_app.plugin_manager.manager import (
    create_plugin_manager,
    load_and_register_plugins,
    get_plugin_registry,
)


def test_skip_gui_only_plugin_when_no_gui(tmp_path: Path, monkeypatch: object) -> None:
    base = tmp_path / "plugins"
    base.mkdir()
    plug = base / "gui_only"
    plug.mkdir()
    (plug / "main.py").write_text("# main", encoding="utf-8")
    (plug / "plugin.toml").write_text(
        """
[plugin]
name = "gui_only"
version = "0.1.0"
compatible_with = ">=0.1.0"

[access]
requires_gui = true
""",
        encoding="utf-8",
    )

    # Force _is_gui_available to False
    monkeypatch.setenv("QT_QPA_PLATFORM", "offscreen")

    pm = create_plugin_manager()
    loaded, skipped = load_and_register_plugins(pm, base)
    assert loaded == 0 and skipped == 1
    reg = get_plugin_registry()
    assert any(r["name"] == "gui_only" and r["status"] == "skipped" for r in reg)


