from pathlib import Path
from typing import List, Dict

from PyQt6.QtWidgets import QDialog, QComboBox, QTextEdit, QLabel, QGridLayout


class TestViewDialog(QDialog):
    def __init__(self, parent, config: Dict[str, str], testcases: List[Path]) -> None:
        super().__init__(parent)
        self.testcases = testcases

        self.config_source = config["sourcecode_filename"]
        self.config_answer = config["answer_filename"]
        self.config_input  = config.get("input_filename", None)

        self.resize(800, 500)
        self.setWindowTitle(f"View Testcases - {len(testcases)} case" + ("s" if len(testcases) > 1 else ""))

        self.layout: QGridLayout = QGridLayout(self)
        self.setLayout(self.layout)

        # region labels
        self.fix_source = QLabel("源代码", self)
        self.layout.addWidget(self.fix_source, 1, 0, 1, 1)

        self.fix_answer = QLabel("参考答案", self)
        self.layout.addWidget(self.fix_answer, 1, 1, 1, 1)

        self.fix_input = QLabel("输入", self)
        self.layout.addWidget(self.fix_input, 1, 2, 1, 1)
        # endregion

        # region text viewers
        self.text_source = QTextEdit(self)
        self.text_source.setReadOnly(True)
        self.layout.addWidget(self.text_source, 2, 0, 1, 1)

        self.text_answer = QTextEdit(self)
        self.text_answer.setReadOnly(True)
        self.layout.addWidget(self.text_answer, 2, 1, 1, 1)

        self.text_input = QTextEdit(self)
        self.text_input.setReadOnly(True)
        self.layout.addWidget(self.text_input, 2, 2, 1, 1)
        # endregion

        # region combo
        self.combo = QComboBox(self)
        self.layout.addWidget(self.combo, 0, 0, 1, 1)
        self.combo.setMaxVisibleItems(10)
        self.combo.setStyleSheet("QComboBox { combobox-popup: 0; }");

        self.combo.currentIndexChanged.connect(self.slot)

        self.combo.addItems(map(lambda p: f"{p.parent.stem} > {p.stem}", self.testcases))
        # endregion

    def slot(self, idx: int):
        self.text_source.setHtml(self.read_code(self.testcases[idx] / self.config_source))
        self.text_answer.setHtml(self.read_code(self.testcases[idx] / self.config_answer))
        if self.config_input is not None:
            self.text_input.setHtml(self.read_code(self.testcases[idx] / self.config_input))

    @staticmethod
    def read_code(path: Path):
        try:
            return "<pre>\n" + path.read_text().replace("<", "&lt;") + "\n</pre>"
        except Exception as e:
            s = repr(e).replace("<", "&lt;")
            return f"<span style='color: red'><code>Cannot read: {s}</code></span>"
