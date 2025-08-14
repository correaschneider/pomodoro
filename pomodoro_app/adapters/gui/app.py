from __future__ import annotations

import sys
from typing import Callable, Optional

from PySide6 import QtCore, QtWidgets

from pomodoro_app.infrastructure.logging import get_logger, setup_logging
from pomodoro_app.infrastructure.i18n import install as install_i18n


logger = get_logger("pomodoro.adapters.gui.app")


def _apply_common_qt_settings(app: QtWidgets.QApplication) -> None:
    """Apply common Qt application settings.

    - Ensure the app does not quit when the last window is closed (tray support)
    - Enable high DPI pixmaps for better rendering on HiDPI displays
    """

    # Qt6 generally manages DPI automatically, but using HiDpi pixmaps helps icons/images
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    # Keep application alive for system tray use; main window close should not exit the app
    QtWidgets.QApplication.setQuitOnLastWindowClosed(False)


def create_app(
    install_translator: Optional[Callable[[QtCore.QCoreApplication], None]] = None,
    app_name: str = "Pomodoro",
    organization_name: str = "PomodoroApp",
    organization_domain: str = "pomodoro.local",
) -> QtWidgets.QApplication:
    """Create and configure the QApplication instance.

    Parameters:
        install_translator: Optional callable to install i18n translator.
            The actual locale loading will be implemented in a future task; this is a hook.
        app_name: Application name for Qt metadata.
        organization_name: Organization name for settings scope.
        organization_domain: Organization domain for settings scope.

    Returns:
        A configured QApplication instance ready to execute.
    """

    # Ensure logging is initialized in case GUI entry is called directly
    setup_logging(app_name="pomodoro_app")

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(app_name)
    app.setOrganizationName(organization_name)
    app.setOrganizationDomain(organization_domain)

    _apply_common_qt_settings(app)

    if install_translator is not None:
        try:
            install_translator(app)
            logger.info("Translator installed via hook")
        except Exception as exc:  # Defensive: do not block GUI on translator issues
            logger.exception("Failed to install translator: %s", exc)
    else:
        # Default: install system locale (or fallback)
        try:
            install_i18n(None)
        except Exception:
            logger.exception("Failed to install default translator")

    logger.info("QApplication created and configured")
    return app


def run_app(
    window_factory: Optional[Callable[[QtWidgets.QApplication], QtWidgets.QWidget]] = None,
    install_translator: Optional[Callable[[QtCore.QCoreApplication], None]] = None,
) -> int:
    """Run the Qt application event loop.

    Parameters:
        window_factory: Optional factory that receives the QApplication and returns
            a top-level QWidget (e.g., MainWindow). If provided, the window is shown.
        install_translator: Optional translator installation hook.

    Returns:
        Process exit code from Qt event loop.
    """

    app = create_app(install_translator=install_translator)

    main_window = None
    if window_factory is not None:
        try:
            main_window = window_factory(app)
            if main_window is not None:
                main_window.show()
                logger.info("Main window created and shown")
        except Exception as exc:
            logger.exception("Failed to create/show main window: %s", exc)

    exit_code = app.exec()
    logger.info("QApplication exited with code %s", exit_code)
    return exit_code


__all__ = [
    "create_app",
    "run_app",
]


