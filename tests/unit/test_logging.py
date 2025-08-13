from __future__ import annotations

import logging
from pathlib import Path

from platformdirs import user_data_dir

from pomodoro_app.infrastructure.logging import setup_logging


def _count_handlers_for(logger: logging.Logger, target_file: Path) -> int:
    count = 0
    for h in logger.handlers:
        if getattr(h, "baseFilename", None) and Path(h.baseFilename) == target_file:
            count += 1
    return count


def test_setup_logging_creates_files(tmp_path: Path) -> None:
    app_name = "pomodoro_app_test_unit1"

    # Ensure a clean logs directory under a temporary HOME for isolation
    # Not strictly necessary when using a unique app_name, but kept explicit
    setup_logging(app_name=app_name)

    log_dir = Path(user_data_dir(app_name)) / "logs"
    assert log_dir.exists() and log_dir.is_dir()
    assert (log_dir / "app.log").exists()
    assert (log_dir / "events.log").exists()
    assert (log_dir / "plugin_errors.log").exists()


def test_setup_logging_is_idempotent(tmp_path: Path) -> None:
    app_name = "pomodoro_app_test_idem"
    setup_logging(app_name=app_name)

    log_dir = Path(user_data_dir(app_name)) / "logs"
    app_log = log_dir / "app.log"
    events_log = log_dir / "events.log"
    plugin_log = log_dir / "plugin_errors.log"

    app_logger = logging.getLogger("pomodoro")
    core_logger = logging.getLogger("pomodoro.core")
    plugin_logger = logging.getLogger("plugin")
    warnings_logger = logging.getLogger("py.warnings")

    before = (
        _count_handlers_for(app_logger, app_log),
        _count_handlers_for(core_logger, events_log),
        _count_handlers_for(plugin_logger, plugin_log),
        _count_handlers_for(warnings_logger, app_log),
    )

    # Call again; should not add duplicate handlers
    setup_logging(app_name=app_name)

    after = (
        _count_handlers_for(app_logger, app_log),
        _count_handlers_for(core_logger, events_log),
        _count_handlers_for(plugin_logger, plugin_log),
        _count_handlers_for(warnings_logger, app_log),
    )

    assert before == after
