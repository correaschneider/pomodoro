from __future__ import annotations

from typing import Callable, Optional

from PySide6 import QtCore, QtWidgets

from pomodoro_app.core.models import TimerState
from pomodoro_app.core.timer_service import TimerService
from pomodoro_app.infrastructure.logging import get_logger

from .bridge import GuiBridge, connect_service_to_bridge
from .main_window import MainWindow


logger = get_logger("pomodoro.adapters.gui.controller")


class GuiController(QtCore.QObject):
    """Controller wiring the MainWindow to TimerService using GuiBridge.

    - Connects UI intents (start/pause/resume/stop) to service methods
    - Subscribes to service events via bridge and updates UI safely
    - Manages button enabled states based on TimerState
    """

    def __init__(
        self,
        window: MainWindow,
        service: TimerService,
        bridge: GuiBridge,
        default_focus_seconds: int = 25 * 60,
    ) -> None:
        super().__init__(window)
        self._window = window
        self._service = service
        self._bridge = bridge
        self._default_focus_seconds = int(default_focus_seconds)
        self._unsubscribe: Optional[Callable[[], None]] = None
        self._stopped: bool = False

        self._wire_ui_to_service()
        self._wire_bridge_to_ui()

    # --- Wiring --------------------------------------------------------------
    def _wire_ui_to_service(self) -> None:
        # Start: duration seconds optional (None uses service defaults)
        self._window.startRequested.connect(self._on_start_requested)  # type: ignore[arg-type]
        self._window.pauseRequested.connect(self._service.pause)
        self._window.resumeRequested.connect(self._service.resume)
        self._window.stopRequested.connect(self._on_stop_requested)
        self._window.settingsRequested.connect(self._show_settings_dialog)

    def _wire_bridge_to_ui(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()
        self._unsubscribe = connect_service_to_bridge(self._service, self._bridge)

        self._bridge.tick.connect(self._on_tick)
        self._bridge.state.connect(self._on_state)
        self._bridge.cycle_end.connect(self._on_cycle_end)

    # --- UI Slots ------------------------------------------------------------
    @QtCore.Slot(object)
    def _on_start_requested(self, duration_s: object | None) -> None:
        # duration_s may be None or int; ignore invalid types defensively
        dur = duration_s if isinstance(duration_s, int) else None
        try:
            self._service.start_focus(dur_s=dur)
        except Exception:
            logger.exception("start_focus failed")

    @QtCore.Slot(int, int, object)
    def _on_tick(self, elapsed: int, remaining: int, state: object) -> None:  # noqa: ARG002
        self._window.update_remaining_seconds(remaining)

    @QtCore.Slot(object)
    def _on_state(self, state: object) -> None:
        # Update status bar and buttons
        self._window.update_state(state)
        self._apply_button_states(state)
        # If transitioned to IDLE due to Stop, reset label to configured focus duration
        try:
            if state == TimerState.IDLE and self._stopped:
                self._window.update_remaining_seconds(self._default_focus_seconds)
                self._stopped = False
        except Exception:
            logger.exception("failed to reset timer label on Stop->IDLE state")

    @QtCore.Slot()
    def _on_stop_requested(self) -> None:
        self._stopped = True
        try:
            self._service.stop()
        except Exception:
            logger.exception("stop failed")

    @QtCore.Slot(object)
    def _on_cycle_end(self, session: object) -> None:  # noqa: ARG002
        # For now, just ensure buttons reflect IDLE after cycle end (state signal also comes)
        self._apply_button_states(TimerState.IDLE)

    @QtCore.Slot()
    def _show_settings_dialog(self) -> None:
        try:
            from .settings_dialog import SettingsDialog

            dlg = SettingsDialog(self._window)
            if dlg.exec() == QtWidgets.QDialog.Accepted:  # type: ignore[attr-defined]
                # Reload defaults after persistence and reflect on UI if idle
                from pomodoro_app.infrastructure.db.connection import connect
                from pomodoro_app.infrastructure.db.schema import ensure_schema
                from pomodoro_app.infrastructure.db.integration import load_settings

                conn = connect()
                ensure_schema(conn)
                settings = load_settings(conn)
                self._default_focus_seconds = int(settings.get("durations", {}).get("focus", 25 * 60))
                if self._service.state == TimerState.IDLE:
                    self._window.update_remaining_seconds(self._default_focus_seconds)
        except Exception:
            logger.exception("failed to open/apply settings dialog")

    # --- Helpers -------------------------------------------------------------
    def _apply_button_states(self, state: object) -> None:
        # Default: conservative disable
        start_enabled = True
        pause_enabled = False
        resume_enabled = False
        stop_enabled = False

        if isinstance(state, TimerState):
            if state in (TimerState.RUNNING_FOCUS, TimerState.RUNNING_BREAK):
                start_enabled = False
                pause_enabled = True
                resume_enabled = False
                stop_enabled = True
            elif state == TimerState.PAUSED:
                start_enabled = False
                pause_enabled = False
                resume_enabled = True
                stop_enabled = True
            elif state == TimerState.IDLE:
                start_enabled = True
                pause_enabled = False
                resume_enabled = False
                stop_enabled = False

        self._window.startButton.setEnabled(start_enabled)
        self._window.pauseButton.setEnabled(pause_enabled)
        self._window.resumeButton.setEnabled(resume_enabled)
        self._window.stopButton.setEnabled(stop_enabled)

    # --- Lifecycle -----------------------------------------------------------
    def dispose(self) -> None:
        if self._unsubscribe:
            self._unsubscribe()
            self._unsubscribe = None


__all__ = ["GuiController"]


