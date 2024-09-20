from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QWidget


class SettingDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
