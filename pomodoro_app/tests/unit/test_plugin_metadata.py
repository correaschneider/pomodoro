from __future__ import annotations

from pathlib import Path

import pytest

from pomodoro_app.plugin_manager.metadata import load_plugin_metadata


def test_load_plugin_metadata_ok(tmp_path: Path) -> None:
    d = tmp_path / "plug"
    d.mkdir()
    (d / "plugin.toml").write_text(
        """
        [plugin]
        name = "demo"
        version = "0.1.0"
        compatible_with = ">=0.1.0"

        [access]
        filesystem = true
        network = false
        requires_gui = true
        """,
        encoding="utf-8",
    )
    meta = load_plugin_metadata(d)
    assert meta.plugin.name == "demo"
    assert meta.access.filesystem is True
    assert meta.access.network is False
    assert meta.access.requires_gui is True


def test_load_plugin_metadata_missing_required(tmp_path: Path) -> None:
    d = tmp_path / "plug"
    d.mkdir()
    (d / "plugin.toml").write_text(
        """
        [plugin]
        name = ""
        version = "0.1.0"
        """,
        encoding="utf-8",
    )
    with pytest.raises(ValueError):
        load_plugin_metadata(d)


