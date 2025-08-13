from __future__ import annotations

import gettext

from PySide6 import QtCore, QtWidgets


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
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QtWidgets.QFormLayout(self)

        self.focusSpin = QtWidgets.QSpinBox(self)
        self.focusSpin.setRange(1, 180)
        self.focusSpin.setValue(25)
        layout.addRow(_("Focus (min)"), self.focusSpin)

        self.breakSpin = QtWidgets.QSpinBox(self)
        self.breakSpin.setRange(1, 60)
        self.breakSpin.setValue(5)
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


__all__ = ["SettingsDialog"]


