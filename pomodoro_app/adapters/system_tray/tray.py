from __future__ import annotations

from typing import Optional, Callable

from PySide6 import QtGui, QtWidgets

from pomodoro_app.core.models import TimerState
from pomodoro_app.adapters.gui.bridge import GuiBridge
from pomodoro_app.adapters.gui.time_utils import format_mm_ss

from pomodoro_app.core.timer_service import TimerService

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.adapters.system_tray")


class TrayController(QtWidgets.QSystemTrayIcon):
    """Base system tray controller with menu scaffold.

    This class provides a minimal QSystemTrayIcon with a context menu scaffold.
    Actions are created but not wired to domain services here; wiring is part of
    later subtasks.
    """

    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget] = None,
        icon: Optional[QtGui.QIcon] = None,
        on_open_settings: Optional[Callable[[], None]] = None,
        on_quit: Optional[Callable[[], None]] = None,
        service: Optional[TimerService] = None,
        main_window: Optional[QtWidgets.QMainWindow] = None,
        bridge: Optional[GuiBridge] = None,
    ) -> None:
        super().__init__(parent)

        self._service = service
        self._main_window = main_window
        self._bridge = bridge
        self._last_remaining: int = 0

        if icon is not None:
            self.setIcon(icon)

        self._menu = QtWidgets.QMenu(parent)

        # Action placeholders; signals wiring and enable/disable logic come later
        self._act_start_focus = self._menu.addAction("Start Focus")
        self._act_start_break = self._menu.addAction("Start Break")
        self._menu.addSeparator()
        self._act_pause = self._menu.addAction("Pause")
        self._act_resume = self._menu.addAction("Resume")
        self._act_stop = self._menu.addAction("Stop")
        self._menu.addSeparator()
        self._act_open_settings = self._menu.addAction("Settings")
        self._act_toggle_window = self._menu.addAction("Show/Hide Window")
        self._menu.addSeparator()
        self._act_quit = self._menu.addAction("Quit")

        if on_open_settings is not None:
            self._act_open_settings.triggered.connect(on_open_settings)  # type: ignore[arg-type]
        if on_quit is not None:
            self._act_quit.triggered.connect(on_quit)  # type: ignore[arg-type]

        # Wiring to TimerService if provided
        if self._service is not None:
            self._act_start_focus.triggered.connect(lambda: self._safe_call(self._service.start_focus))  # type: ignore[arg-type]
            self._act_start_break.triggered.connect(lambda: self._safe_call(self._service.start_break))  # type: ignore[arg-type]
            self._act_pause.triggered.connect(lambda: self._safe_call(self._service.pause))  # type: ignore[arg-type]
            self._act_resume.triggered.connect(lambda: self._safe_call(self._service.resume))  # type: ignore[arg-type]
            self._act_stop.triggered.connect(lambda: self._safe_call(self._service.stop))  # type: ignore[arg-type]
        else:
            # Disable actions that require wiring when service is absent
            self._act_start_focus.setEnabled(False)
            self._act_start_break.setEnabled(False)
            self._act_pause.setEnabled(False)
            self._act_resume.setEnabled(False)
            self._act_stop.setEnabled(False)

        # Toggle main window visibility if provided
        if self._main_window is not None:
            self._act_toggle_window.triggered.connect(self._toggle_main_window)  # type: ignore[arg-type]
        else:
            self._act_toggle_window.setEnabled(False)

        # Live tooltip via GuiBridge
        if self._bridge is not None:
            self._bridge.tick.connect(self._on_tick)
            self._bridge.state.connect(self._on_state)

        self.setContextMenu(self._menu)
        self.setToolTip("Pomodoro")

        logger.info("System tray initialized with menu and wiring")

    # Helpers
    def _safe_call(self, fn: Callable[[], None]) -> None:
        try:
            fn()
        except Exception:
            logger.exception("action failed")

    def _toggle_main_window(self) -> None:
        try:
            assert self._main_window is not None
            if self._main_window.isVisible():
                self._main_window.hide()
            else:
                self._main_window.show()
                self._main_window.raise_()
                self._main_window.activateWindow()
        except Exception:
            logger.exception("toggle window failed")

    # Tooltip updates ---------------------------------------------------------
    def _on_tick(self, elapsed: int, remaining: int, state: object) -> None:  # noqa: ARG002
        self._last_remaining = int(remaining)
        self._update_tooltip(state, self._last_remaining)

    def _on_state(self, state: object) -> None:
        # Update tooltip using last known remaining seconds
        self._update_tooltip(state, self._last_remaining)

    def _update_tooltip(self, state: object, remaining: int) -> None:
        try:
            state_name = state.name if isinstance(state, TimerState) else str(state)
            self.setToolTip(f"{state_name} – {format_mm_ss(remaining)}")
        except Exception:
            logger.exception("failed to update tooltip")

    # Expose actions for later wiring/toggling in subsequent subtasks
    @property
    def act_start_focus(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_start_focus

    @property
    def act_start_break(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_start_break

    @property
    def act_pause(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_pause

    @property
    def act_resume(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_resume

    @property
    def act_stop(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_stop

    @property
    def act_open_settings(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_open_settings

    @property
    def act_toggle_window(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_toggle_window

    @property
    def act_quit(self) -> QtGui.QAction:  # type: ignore[override]
        return self._act_quit


__all__ = ["TrayController"]


