from pathlib import Path
from json import loads
from difflib import HtmlDiff

from PyQt6.QtWidgets import QDialog, QGridLayout, QComboBox, QLabel, QTextBrowser

from gui.helper import Testcase, Configure


class HistoryDialog(QDialog):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.setWindowTitle("Judge History")
        self.resize(800, 500)

        self.layout: QGridLayout = QGridLayout(self)
        self.setLayout(self.layout)

        # region pick a test
        self.combo_judge = QComboBox(self)
        self.layout.addWidget(self.combo_judge, 0, 0, 1, 3)
        self.combo_judge.setMaxVisibleItems(10)
        self.combo_judge.setStyleSheet("QComboBox { combobox-popup: 0; }");

        self.combo_testcase = QComboBox(self)
        self.layout.addWidget(self.combo_testcase, 0, 3, 1, 3)
        self.combo_testcase.setMaxVisibleItems(10)
        self.combo_testcase.setStyleSheet("QComboBox { combobox-popup: 0; }");
        # endregion

        # region testcase info label
        self.fix_source = QLabel("源代码", self)
        self.layout.addWidget(self.fix_source, 1, 0, 1, 2)

        self.fix_input = QLabel("输入", self)
        self.layout.addWidget(self.fix_input, 1, 2, 1, 2)

        self.fix_info = QLabel("测评结果", self)
        self.layout.addWidget(self.fix_info, 1, 4, 1, 2)

        self.fix_stdout = QLabel("标准输出", self)
        self.layout.addWidget(self.fix_stdout, 3, 4, 1, 2)

        self.fix_stderr = QLabel("标准错误输出", self)
        self.layout.addWidget(self.fix_stderr, 5, 4, 1, 2)

        self.fix_diff = QLabel("差异比较（使用 Ctrl+滚轮 可缩放字体，点击行号前的字母可跳转至差异）", self)
        self.layout.addWidget(self.fix_diff, 7, 0, 1, 6)
        # endregion

        # region testcase info text
        self.disp_source = QTextBrowser(self)
        self.layout.addWidget(self.disp_source, 2, 0, 5, 2)

        self.disp_input = QTextBrowser(self)
        self.layout.addWidget(self.disp_input, 2, 2, 5, 2)

        self.disp_info = QTextBrowser(self)
        self.layout.addWidget(self.disp_info, 2, 4, 1, 2)

        self.disp_stdout = QTextBrowser(self)
        self.layout.addWidget(self.disp_stdout, 4, 4, 1, 2)

        self.disp_stderr = QTextBrowser(self)
        self.layout.addWidget(self.disp_stderr, 6, 4, 1, 2)

        self.disp_diff = QTextBrowser(self)
        self.layout.addWidget(self.disp_diff, 8, 0, 1, 6)
        self.layout.setRowMinimumHeight(8, 200)
        # endregion

        self.judges = []
        self.testcases = []

        # region signal & slot
        self.combo_judge.currentIndexChanged.connect(self.slot_update_testcase)
        self.combo_testcase.currentIndexChanged.connect(self.slot_update_detail)
        # endregion

        self.startup()

    def startup(self):
        self.get_judge_record()
        self.combo_judge.addItems(map(self.read_summary, self.judges))

    def get_judge_record(self):
        self.judges = []
        if not Path("results").is_dir():
            return
        for result in Path("results").glob("*/"):
            self.judges.append(result)
        self.judges.sort(key=str, reverse=True)

    def read_summary(self, result: Path) -> str:
        try:
            summary = (result / "summary.txt").read_text(encoding="utf-8", errors="replace")
            try:
                obj = loads(summary)
                return (
                    f"{result.stem} > " + obj["Mode"].replace("_", " ").title() +
                    " WA(" + str(obj["WA"]) + ")" +
                    " TLE(" + str(obj["TLE"]) + ")" +
                    " RE(" + str(obj["RE"]) + ")")
            except:
                return f"{result.stem} > " + summary.splitlines()[-1].replace('\t', ", ")
        except:
            return f"{result.stem} > N/A"

    def slot_update_testcase(self, idx):
        self.combo_testcase.disconnect()
        self.combo_testcase.clear()
        self.combo_testcase.currentIndexChanged.connect(self.slot_update_detail)
        self.testcases = Testcase.get_list(self.judges[idx])
        self.combo_testcase.addItems(map(lambda p: self.get_testcase_desc(idx, p), self.testcases))

    def slot_update_detail(self, idx):
        self.disp_source.setHtml(self.try_read_code(
            self.get_path_in_testcase("sourcecode_filename")
        ))
        self.disp_input.setHtml(self.try_read_code(
            self.get_path_in_testcase("input_filename")
        ))
        self.disp_info.setHtml(self.try_read_code(
            self.testcases[idx] / "info.txt"
        ))
        self.disp_stdout.setHtml(self.try_read_code(
            self.testcases[idx] / "stdout.txt"
        ))
        self.disp_stderr.setHtml(self.try_read_code(
            self.testcases[idx] / "stderr.txt"
        ))
        answer = self.try_read(self.get_path_in_testcase("answer_filename"))
        output = self.try_read(self.testcases[idx] / Path(Configure.get_config()["stage"][Configure.get_var("mode")]["compiler_output_file"]))
        self.disp_diff.setStyleSheet("QTextBrowser { background-color: white; color: black }")
        self.disp_diff.setHtml(
            HtmlDiff().make_file(answer.splitlines(), output.splitlines())
        )

    def get_testcase_desc(self, judge_idx, path: Path) -> str:
        base = str(path.relative_to(self.judges[judge_idx]))
        try:
            info = (path / "info.txt").read_text(encoding="utf-8", errors="replace").splitlines()
            if info[0].startswith(">>>"):
                return f"{base} > " + info[1].removeprefix(">>> ")
            return f"{base} > {info[0]}"
        except:
            return f"{base} > N/A"

    def get_path_in_testcase(self, item: str) -> Path:
        relate_path = self.testcases[self.combo_testcase.currentIndex()] \
                          .relative_to(self.judges[self.combo_judge.currentIndex()])
        return (
            Path(Configure.get_config()["stage"][Configure.get_var("mode")]["testfile_path"]) /
            relate_path /
            Configure.get_config()["stage"][Configure.get_var("mode")].get(item, "")
        )

    @staticmethod
    def escape(s: str) -> str:
        return s.replace("<", "&lt;")

    @staticmethod
    def try_read_code(path: Path) -> str:
        try:
            content = HistoryDialog.escape(path.read_text(encoding="utf-8", errors="replace"))
            if content == "":
                return "<code>&lt; Empty ></code>"
            return f"<pre>\n{content}\n</pre>"
        except:
            return "<code>&lt; Not Found ></code>"
    
    @staticmethod
    def try_read(path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            return f"Cannot read {path} in that: {repr(e)}"
