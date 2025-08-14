from __future__ import annotations

import argparse
import sys
import logging

from pomodoro_app.infrastructure.logging import setup_logging, get_logger
from pomodoro_app.core.timer_service import TimerService
from pomodoro_app.infrastructure.db.connection import connect
from pomodoro_app.infrastructure.db.schema import ensure_schema
from pomodoro_app.infrastructure.db.integration import wire_persistence, load_settings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="pomodoro-app")
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Emite mensagens de log de exemplo e sai com código 0",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Inicia a interface gráfica (Qt MainWindow)",
    )
    args = parser.parse_args(argv)

    setup_logging(app_name="pomodoro_app")

    app_logger = logging.getLogger("pomodoro")
    core_logger = logging.getLogger("pomodoro.core")

    app_logger.info("Startup: pomodoro initialized")
    core_logger.info("Startup: core initialized")

    # Precedência: --smoke > --gui
    if args.smoke:
        if args.gui:
            logging.getLogger("pomodoro").info("--smoke especificado; ignorando --gui")
        app_logger.info("Smoke: application logger OK")
        core_logger.info("Smoke: core logger OK")
        plugin_demo_logger = logging.getLogger("plugin.demo")
        plugin_demo_logger.error("Smoke: demo plugin error (expected)")
        return 0

    if args.gui:
        # Checagem básica de disponibilidade de display (Linux/Unix)
        try:
            import os, sys as _sys

            if _sys.platform.startswith("linux"):
                has_display = bool(os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY") or os.environ.get("QT_QPA_PLATFORM"))
                if not has_display:
                    print(
                        "GUI not available: no display (DISPLAY/WAYLAND_DISPLAY not set) and no offscreen platform configured",
                        file=__import__("sys").stderr,
                    )
                    return 2
        except Exception:
            pass

        # Import lazy da GUI para evitar custo quando não necessário
        from pomodoro_app.adapters.gui.app import run_app  # type: ignore
        from pomodoro_app.adapters.gui.main_window import MainWindow  # type: ignore
        from pomodoro_app.adapters.gui.bridge import GuiBridge  # type: ignore
        from pomodoro_app.adapters.gui.controller import GuiController  # type: ignore
        from pomodoro_app.core.timer_service import TimerService  # type: ignore

        # Carregar configurações para obter duração padrão de focus
        conn = connect()
        ensure_schema(conn)
        settings = load_settings(conn)
        default_focus = int(settings.get("durations", {}).get("focus", 25 * 60))

        service = TimerService()
        bridge = GuiBridge()

        def _factory(_app: object) -> object:
            win = MainWindow()
            # Wire controller so that Play/Pause/Resume/Stop control the service
            GuiController(win, service, bridge, default_focus_seconds=default_focus)
            return win

        return int(run_app(_factory))

    # Minimal wiring for persistence and service lifecycle (no GUI bootstrap here)
    conn = connect()
    ensure_schema(conn)
    settings = load_settings(conn)

    service = TimerService()
    unsubscribe = wire_persistence(service, conn)
    try:
        app_logger.info("TimerService and persistence wiring initialized")
    finally:
        # Ensure clean unsubscribe on exit path
        unsubscribe()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
