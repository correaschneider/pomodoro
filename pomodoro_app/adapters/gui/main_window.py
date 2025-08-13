from __future__ import annotations

import gettext

from PySide6 import QtCore, QtGui, QtWidgets

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.adapters.gui.main_window")
_ = gettext.gettext


class MainWindow(QtWidgets.QMainWindow):
    """Main application window with timer display and controls.

    Emits UI intent signals to be handled by a controller in a later subtask.
    """

    # UI intent signals (controller will connect to these)
    startRequested = QtCore.Signal(object)  # Optional[int] duration seconds; None for defaults
    pauseRequested = QtCore.Signal()
    resumeRequested = QtCore.Signal()
    stopRequested = QtCore.Signal()
    settingsRequested = QtCore.Signal()
    gracefulStopRequested = QtCore.Signal()  # Emitted when user intends to quit app

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(_("Pomodoro"))
        self._tray_enabled = False
        self._build_ui()
        self._connect_ui_signals()

    # --- UI construction -----------------------------------------------------
    def _build_ui(self) -> None:
        self._create_actions()
        self._create_menubar()
        self._create_statusbar()

        central = QtWidgets.QWidget(self)
        layout = QtWidgets.QVBoxLayout(central)

        # Timer label
        self.timerLabel = QtWidgets.QLabel("00:00", self)
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        self.timerLabel.setFont(font)
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.timerLabel, alignment=QtCore.Qt.AlignCenter)

        # Controls
        controls = QtWidgets.QHBoxLayout()
        self.startButton = QtWidgets.QPushButton(_("Start"), self)
        self.pauseButton = QtWidgets.QPushButton(_("Pause"), self)
        self.resumeButton = QtWidgets.QPushButton(_("Resume"), self)
        self.stopButton = QtWidgets.QPushButton(_("Stop"), self)

        controls.addWidget(self.startButton)
        controls.addWidget(self.pauseButton)
        controls.addWidget(self.resumeButton)
        controls.addWidget(self.stopButton)
        layout.addLayout(controls)

        self.setCentralWidget(central)

        # Initial enabled state (controller will refine in subtask 3.4)
        self.pauseButton.setEnabled(True)
        self.resumeButton.setEnabled(True)
        self.stopButton.setEnabled(True)

    def _create_actions(self) -> None:
        self.settingsAction = QtGui.QAction(_("Settings"), self)
        self.settingsAction.setShortcut(QtGui.QKeySequence("Ctrl+,"))

    def _create_menubar(self) -> None:
        menubar = self.menuBar()
        app_menu = menubar.addMenu(_("App"))
        app_menu.addAction(self.settingsAction)

    def _create_statusbar(self) -> None:
        self.statusBar().showMessage(_("Ready"))

    # --- UI signal wiring ----------------------------------------------------
    def _connect_ui_signals(self) -> None:
        self.startButton.clicked.connect(lambda: self.startRequested.emit(None))
        self.pauseButton.clicked.connect(self.pauseRequested.emit)
        self.resumeButton.clicked.connect(self.resumeRequested.emit)
        self.stopButton.clicked.connect(self.stopRequested.emit)
        self.settingsAction.triggered.connect(self.settingsRequested.emit)

        # Default handler to show a simple settings dialog
        # Controller can override by disconnecting/reconnecting this signal
        self.settingsRequested.connect(self._show_settings_dialog)

    # --- Public update hooks (controller/bridge will call later) -------------
    @QtCore.Slot(int)
    def update_remaining_seconds(self, remaining: int) -> None:
        # Minimal representation; time utility and formatting will be added in subtask 3.5
        try:
            minutes = max(0, remaining) // 60
            seconds = max(0, remaining) % 60
            self.timerLabel.setText(f"{minutes:02d}:{seconds:02d}")
        except Exception:
            logger.exception("failed to update remaining seconds")

    @QtCore.Slot(object)
    def update_state(self, state: object) -> None:
        # Controller will improve enable/disable logic in subtask 3.4
        self.statusBar().showMessage(_(f"State: {getattr(state, 'name', state)}"))

    # --- Default handlers ----------------------------------------------------
    @QtCore.Slot()
    def _show_settings_dialog(self) -> None:
        try:
            from .settings_dialog import SettingsDialog

            dlg = SettingsDialog(self)
            dlg.exec()
        except Exception:
            logger.exception("failed to open settings dialog")

    # --- Tray integration helpers -------------------------------------------
    def setTrayEnabled(self, enabled: bool) -> None:
        self._tray_enabled = bool(enabled)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:  # type: ignore[override]
        # If tray is enabled, hide to tray instead of quitting
        if self._tray_enabled:
            event.ignore()
            self.hide()
            self.statusBar().showMessage(_("Hidden to tray"))
            return

        # Otherwise, request graceful stop so controller can shutdown services
        try:
            self.gracefulStopRequested.emit()
        except Exception:
            logger.exception("failed emitting gracefulStopRequested")
        event.accept()


__all__ = ["MainWindow"]


