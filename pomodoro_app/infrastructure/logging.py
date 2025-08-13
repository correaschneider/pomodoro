from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from platformdirs import user_data_dir


def _ensure_directory_exists(directory_path: Path) -> None:
    """Create directory and parents if they do not exist."""
    directory_path.mkdir(parents=True, exist_ok=True)


def _create_rotating_file_handler(file_path: Path) -> RotatingFileHandler:
    """Create a RotatingFileHandler with the project standard configuration."""
    handler = RotatingFileHandler(
        filename=str(file_path),
        maxBytes=1_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    return handler


def _logger_has_handler_for_path(logger: logging.Logger, target_file: Path) -> bool:
    """Check if the logger already has a RotatingFileHandler pointing to target_file."""
    for existing in logger.handlers:
        if isinstance(existing, RotatingFileHandler):
            try:
                if Path(existing.baseFilename) == target_file:
                    return True
            except Exception:
                # Be defensive: if baseFilename is inaccessible for any reason, ignore.
                continue
    return False


def setup_logging(app_name: str = "pomodoro_app") -> None:
    """
    Configure centralized logging with rotating file handlers.

    - Logs directory: user data dir for the application, under "logs" subdirectory
    - Files and namespaces:
      - app.log      -> logger name prefix: "pomodoro"
      - events.log   -> logger name prefix: "pomodoro.core"
      - plugin_errors.log -> logger name prefix: "plugin"
    - Rotating handlers: 1MB per file, 5 backups, UTF-8 encoding
    - Idempotent: repeated calls do not duplicate handlers
    - Warnings are captured into app.log
    """

    logs_base_dir = Path(user_data_dir(app_name)) / "logs"
    _ensure_directory_exists(logs_base_dir)

    app_log_path = logs_base_dir / "app.log"
    events_log_path = logs_base_dir / "events.log"
    plugin_errors_log_path = logs_base_dir / "plugin_errors.log"

    app_logger = logging.getLogger("pomodoro")
    core_logger = logging.getLogger("pomodoro.core")
    plugin_logger = logging.getLogger("plugin")

    app_logger.setLevel(logging.INFO)
    core_logger.setLevel(logging.INFO)
    plugin_logger.setLevel(logging.INFO)

    if not _logger_has_handler_for_path(app_logger, app_log_path):
        app_logger.addHandler(_create_rotating_file_handler(app_log_path))

    if not _logger_has_handler_for_path(core_logger, events_log_path):
        core_logger.addHandler(_create_rotating_file_handler(events_log_path))

    # Avoid duplicating plugin errors into parents unless explicitly desired
    plugin_logger.propagate = False
    if not _logger_has_handler_for_path(plugin_logger, plugin_errors_log_path):
        plugin_logger.addHandler(_create_rotating_file_handler(plugin_errors_log_path))

    # Capture warnings and ensure they go to app.log as well
    logging.captureWarnings(True)
    warnings_logger = logging.getLogger("py.warnings")
    warnings_logger.setLevel(logging.WARNING)
    if not _logger_has_handler_for_path(warnings_logger, app_log_path):
        warnings_logger.addHandler(_create_rotating_file_handler(app_log_path))


