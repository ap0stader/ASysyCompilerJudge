from typing import Literal
from json import JSONDecodeError

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QMainWindow, QGridLayout, QWidget, QPushButton, QLabel, QLineEdit,
                             QButtonGroup, QRadioButton, QGroupBox, QVBoxLayout, QProgressBar,
                             QTextEdit)


from gui.helper import get_version
from gui.helper import StringWrapper as W
from gui.helper import Configure

from gui.setting_dialog import SettingDialog


class MainWidget(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.resize(600, 400)
        self.setWindowTitle("A Sysy-Compiler Judge  V" + get_version())

        # region main layout
        self.widget = QWidget(self)
        self.layout: QGridLayout = QGridLayout(self.widget)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        # endregion

        # region functional buttons
        self.btn_settings = QPushButton("设置", self.widget)
        self.layout.addWidget(self.btn_settings, 0, 0, 1, 2)

        self.btn_switch = QPushButton("启动测评", self.widget)
        self.layout.addWidget(self.btn_switch, 1, 0, 1, 2)

        self.btn_history = QPushButton("测评记录", self.widget)
        self.layout.addWidget(self.btn_history, 2, 0, 1, 2)
        # endregion

        # region choose the test
        self.btn_group_hw = QButtonGroup(self.widget)

        self.group_hw = QGroupBox("测评内容", self.widget)
        self.group_hw_layout = QVBoxLayout(self.group_hw)
        self.layout.addWidget(self.group_hw, 3, 0, 1, 2)

        self.radio_lexer = QRadioButton("词法分析", self.group_hw)
        self.btn_group_hw.addButton(self.radio_lexer)
        self.group_hw_layout.addWidget(self.radio_lexer)
        self.radio_lexer.setChecked(True)  # TODO: Store the last choise

        self.radio_syntax = QRadioButton("语法分析", self.group_hw)
        self.btn_group_hw.addButton(self.radio_syntax)
        self.group_hw_layout.addWidget(self.radio_syntax)

        self.radio_semantic = QRadioButton("语义分析", self.group_hw)
        self.btn_group_hw.addButton(self.radio_semantic)
        self.group_hw_layout.addWidget(self.radio_semantic)
        self.radio_semantic.setDisabled(True)  # TODO: Support it

        self.radio_codegen = QRadioButton("代码生成", self.group_hw)
        self.btn_group_hw.addButton(self.radio_codegen)
        self.group_hw_layout.addWidget(self.radio_codegen)
        self.radio_codegen.setDisabled(True)  # TODO: Support it

        # TODO: Different code gen
        # endregion

        # region dashboard header
        self.fix_target_file = QLabel("目标文件", self.widget)
        self.layout.addWidget(self.fix_target_file, 0, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.disp_target_file = QLineEdit("N/A", self.widget)
        self.disp_target_file.setReadOnly(True)
        self.layout.addWidget(self.disp_target_file, 0, 4, 1, 2)

        self.fix_modify_time = QLabel("修改于", self.widget)
        self.layout.addWidget(self.fix_modify_time, 0, 6, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.disp_modify_time = QLineEdit("N/A", self.widget)
        self.disp_modify_time.setReadOnly(True)
        self.layout.addWidget(self.disp_modify_time, 0, 7, 1, 2)
        # endregion

        # region watchdog info
        self.fix_watchdog = QLabel("WatchDog", self.widget)
        self.layout.addWidget(self.fix_watchdog, 1, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.disp_watchdog = QLineEdit("N/A", self.widget)
        self.disp_watchdog.setReadOnly(True)
        self.layout.addWidget(self.disp_watchdog, 1, 4, 1, 2)

        self.btn_force_test = QPushButton("立即进行测评", self.widget)
        self.layout.addWidget(self.btn_force_test, 1, 6, 1, 3)
        # endregion

        # region progress
        self.progress = QProgressBar(self.widget)
        self.progress.setValue(0)
        self.layout.addWidget(self.progress, 2, 3, 1, 6)

        self.group_info = QGroupBox("测评信息", self.widget)
        self.group_info_layout = QVBoxLayout(self.group_info)
        self.layout.addWidget(self.group_info, 3, 3, 1, 6)

        self.text_info = QTextEdit(self.group_info)
        self.text_info.setReadOnly(True)
        self.group_info_layout.addWidget(self.text_info)
        # endregion

        # region signal & slot
        self.btn_settings.clicked.connect(self.slot_setting)
        self.btn_switch.clicked.connect(lambda: self.unimplemented("switch"))
        self.btn_history.clicked.connect(lambda: self.unimplemented("history"))
        self.btn_force_test.clicked.connect(lambda: self.unimplemented("force-test"))
        # endregion

        self.startup()

    def slot_setting(self):
        self.append_info("Open Settings ...")
        SettingDialog(self).exec()
        self.append_info("Re-read settings ...")
        Configure.reset()
        self.startup()

    def unimplemented(self, of: str = ""):
        self.append_info("Unimplemented" + (f": {W.code(of)}" if of else ""), "warn")

    def append_info(self, line: str, type: Literal["info", "warn", "crit"] = "info"):
        style = {
            "info": "",
            "warn": "style='color: yellow'",
            "crit": "style='color: red'"
        }
        self.text_info.append(f"<span {style[type]}><code>{type}> </code>{line}</span>")

    def startup(self):
        if not Configure.file_exist():
            self.append_info("配置文件残缺", "crit")
            self.append_info("请首先执行 " + W.code("init.py") + " 或参照 " + W.code("config_example/") + " 进行修复")
            self.disable_everything()
            return
        try:
            _ = Configure.get_config(self.append_info)
        except UnicodeDecodeError as e:
            self.append_info("配置文件编码错误: " + W.code(repr(e)), "crit")
            self.append_info("请使用 " + W.code("UTF-8") + " 编码")
            self.disable_everything()
            return
        except JSONDecodeError as e:
            self.append_info("Json 文件解码错误: " + W.code(repr(e)), "crit")
            self.disable_everything()
            return
        if not Configure.verify(lambda s: self.append_info("配置文件残缺: " + W.code(s), "crit")):
            self.append_info("请参照 " + W.code("config_example/") + " 进行修复")
            self.disable_everything()
            self.btn_settings.setDisabled(False)  # Allow user to modify the setting
            return
        self.recover_everything()

    def disable_everything(self):
        self.append_info("禁用全局交互 ...", "warn")
        for child in (child for child in self.widget.children() if isinstance(child, QWidget)):
            child.setDisabled(True)

    def recover_everything(self):
        for child in (child for child in self.widget.children() if isinstance(child, QWidget)):
            child.setDisabled(False)
