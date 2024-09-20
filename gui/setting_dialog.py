import json

from PyQt6.QtGui import QTextOption
from PyQt6.QtWidgets import QDialog, QGridLayout, QPushButton, QTextEdit

from gui.helper import Configure


class SettingDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(300, 500)

        self.layout: QGridLayout = QGridLayout(self)
        self.setLayout(self.layout)

        self.files = ["lang", "stage", "command"]
        self.btns = []

        for i, name in enumerate(self.files):
            btn = QPushButton(name, self)
            self.layout.addWidget(btn, 0, i, 1, 1)
            btn.clicked.connect(self.build_slot_btn_clicked(i))
            self.btns.append(btn)

        self.config_editor = QTextEdit(self)
        self.config_editor.setDisabled(True)
        self.config_editor.setWordWrapMode(QTextOption.WrapMode.NoWrap)
        self.layout.addWidget(self.config_editor, 1, 0, len(self.files), 0)

        self.editor_connect = None

    def build_slot_btn_clicked(self, i):
        def inner():
            for btn in self.btns:
                btn.setDisabled(False)
            self.btns[i].setDisabled(True)
            if self.editor_connect is not None:
                self.config_editor.disconnect(self.editor_connect)
                self.editor_connect = None
            self.config_editor.setPlainText(Configure.read_config_file(self.files[i]))
            self.config_editor.setDisabled(False)
            self.editor_connect = self.config_editor.textChanged.connect(
                lambda: Configure.write_config_file(self.files[i], self.config_editor.toPlainText())
            )
        return inner
