from __future__ import annotations

from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets

from pomodoro_app.infrastructure.logging import get_logger


logger = get_logger("pomodoro.adapters.notifications.overlay")


class QtOverlay(QtWidgets.QWidget):
    """Frameless, translucent overlay widget for brief notifications."""

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None, duration_ms: int = 2000) -> None:
        super().__init__(parent)
        self._duration_ms = max(0, int(duration_ms))
        self._enabled: bool = True

        self.setWindowFlags(
            QtCore.Qt.Tool | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        self._label = QtWidgets.QLabel("", self)
        self._label.setAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        self._label.setFont(font)
        self._label.setStyleSheet("color: white;")
        layout.addWidget(self._label)

        # Rounded semi-transparent background
        self.setStyleSheet(
            "background-color: rgba(0, 0, 0, 180); border-radius: 10px;"
        )

        self._timer = QtCore.QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.timeout.connect(self.hide)

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool) -> None:
        self._enabled = bool(value)

    def show_message(self, title: str, message: str) -> None:
        if not self._enabled:
            return
        try:
            text = title if not message else f"{title}\n{message}"
            self._label.setText(text)
            self.adjustSize()
            # Center on screen if no parent
            geo = QtWidgets.QApplication.primaryScreen().availableGeometry()  # type: ignore[assignment]
            self.move(
                geo.center().x() - self.width() // 2,
                geo.center().y() - self.height() // 2,
            )
            self.show()
            if self._duration_ms > 0:
                self._timer.start(self._duration_ms)
        except Exception:
            logger.exception("failed to show overlay message")


__all__ = ["QtOverlay"]


