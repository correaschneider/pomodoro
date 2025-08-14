from __future__ import annotations

from typing import Optional, Callable

from PySide6 import QtGui, QtWidgets

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
    ) -> None:
        super().__init__(parent)

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

        self.setContextMenu(self._menu)
        self.setToolTip("Pomodoro")

        logger.info("System tray initialized with base menu")

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


