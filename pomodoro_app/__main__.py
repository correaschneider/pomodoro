from __future__ import annotations

import argparse
import sys
import logging

from pomodoro_app.infrastructure.logging import setup_logging, get_logger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pomodoro-app")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Emite mensagens de log de exemplo e sai com código 0",
    )
    args = parser.parse_args(argv)

    setup_logging(app_name="pomodoro_app")

    app_logger = logging.getLogger("pomodoro")
    core_logger = logging.getLogger("pomodoro.core")

    app_logger.info("Startup: pomodoro initialized")
    core_logger.info("Startup: core initialized")

    if args.smoke:
        app_logger.info("Smoke: application logger OK")
        core_logger.info("Smoke: core logger OK")
        plugin_demo_logger = logging.getLogger("plugin.demo")
        plugin_demo_logger.error("Smoke: demo plugin error (expected)")
        return 0

    # Placeholder: inicialização futura de GUI/CLI
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


