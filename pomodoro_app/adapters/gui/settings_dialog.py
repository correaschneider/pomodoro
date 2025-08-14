from __future__ import annotations

import gettext

from PySide6 import QtCore, QtWidgets

from pomodoro_app.infrastructure.db.connection import connect
from pomodoro_app.infrastructure.db.schema import ensure_schema
from pomodoro_app.infrastructure.db.repositories import SettingsRepository


_ = gettext.gettext


class SettingsDialog(QtWidgets.QDialog):
    """Basic settings stub (no persistence yet).

    Fields:
      - Focus duration (minutes)
      - Break duration (minutes)
      - Language (placeholder)
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(_("Settings"))
        # Persistence
        self._conn = connect()
        ensure_schema(self._conn)
        self._repo = SettingsRepository(self._conn)
        self._build_ui()
        self._load_values()

    def _build_ui(self) -> None:
        layout = QtWidgets.QFormLayout(self)

        self.focusSpin = QtWidgets.QSpinBox(self)
        self.focusSpin.setRange(1, 180)
        layout.addRow(_("Focus (min)"), self.focusSpin)

        self.breakSpin = QtWidgets.QSpinBox(self)
        self.breakSpin.setRange(1, 60)
        layout.addRow(_("Break (min)"), self.breakSpin)

        self.langCombo = QtWidgets.QComboBox(self)
        self.langCombo.addItems(["system", "en", "pt_BR"])  # placeholder
        layout.addRow(_("Language"), self.langCombo)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            parent=self,
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def _load_values(self) -> None:
        try:
            durations = self._repo.get("durations", {"focus": 25 * 60, "break": 5 * 60}) or {}
            focus_s = int(durations.get("focus", 25 * 60))
            break_s = int(durations.get("break", 5 * 60))
            self.focusSpin.setValue(max(1, focus_s // 60))
            self.breakSpin.setValue(max(1, break_s // 60))
        except Exception:
            # Fallback to defaults
            self.focusSpin.setValue(25)
            self.breakSpin.setValue(5)
        try:
            language = self._repo.get("language", "system") or "system"
            idx = max(0, self.langCombo.findText(str(language)))
            self.langCombo.setCurrentIndex(idx)
        except Exception:
            pass

    def get_values(self) -> tuple[int, int, str]:
        return (
            int(self.focusSpin.value()) * 60,
            int(self.breakSpin.value()) * 60,
            str(self.langCombo.currentText()),
        )

    def accept(self) -> None:  # type: ignore[override]
        # Persist values
        focus_s, break_s, language = self.get_values()
        try:
            self._repo.set("durations", {"focus": focus_s, "break": break_s})
            self._repo.set("language", language)
        except Exception:
            # Keep dialog open? For now, still close but values might not persist
            pass
        super().accept()


__all__ = ["SettingsDialog"]


