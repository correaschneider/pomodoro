from __future__ import annotations

from pathlib import Path

from pomodoro_app.plugin_manager.manager import (
    get_plugins_base_dir,
    discover_plugin_folders,
    create_plugin_manager,
)


def test_discover_plugin_folders_looks_for_main_py(tmp_path: Path, monkeypatch: object) -> None:
    base = tmp_path / "plugins"
    (base / "good").mkdir(parents=True)
    (base / "good" / "main.py").write_text("# plugin main", encoding="utf-8")
    (base / "bad").mkdir(parents=True)
    # missing main.py

    # Redirect discovery base dir
    monkeypatch.setenv("HOME", str(tmp_path))  # platformdirs reads HOME

    found = discover_plugin_folders(base)
    assert len(found) == 1
    assert found[0].name == "good"


def test_create_plugin_manager_has_hookspecs() -> None:
    pm = create_plugin_manager()
    # Ensure hookspecs were added (by checking for one of them)
    assert hasattr(pm.hook, "on_app_start")


