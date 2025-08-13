from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from platformdirs import user_data_dir


def test_smoke_mode_writes_expected_logs(tmp_path: Path) -> None:
    # Run module in a subprocess with HOME pointing to a temp directory so logs are isolated
    env = os.environ.copy()
    env["HOME"] = str(tmp_path)
    env["PYTHONPATH"] = os.getcwd()

    proc = subprocess.run(
        [sys.executable, "-m", "pomodoro_app", "--smoke"],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )

    assert proc.returncode == 0, proc.stderr

    # Compute the log directory using the same HOME as the subprocess
    # platformdirs reads HOME at call time, so set it temporarily
    old_home = os.environ.get("HOME")
    try:
        os.environ["HOME"] = str(tmp_path)
        log_dir = Path(user_data_dir("pomodoro_app")) / "logs"
    finally:
        if old_home is not None:
            os.environ["HOME"] = old_home
        else:
            os.environ.pop("HOME", None)

    app_log = log_dir / "app.log"
    events_log = log_dir / "events.log"
    plugin_log = log_dir / "plugin_errors.log"

    assert app_log.exists()
    assert events_log.exists()
    assert plugin_log.exists()

    app_text = app_log.read_text(encoding="utf-8")
    events_text = events_log.read_text(encoding="utf-8")
    plugin_text = plugin_log.read_text(encoding="utf-8")

    assert "Startup: pomodoro initialized" in app_text
    assert "Startup: core initialized" in events_text
    assert "demo plugin error" in plugin_text
