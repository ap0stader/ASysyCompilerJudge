import time
import shutil
from typing import Tuple
from pathlib import Path
from subprocess import call, TimeoutExpired
from json import dumps

from PyQt6.QtCore import pyqtSignal, QThread

from util import StatusCode
from judge import LineCompare
from gui.helper import StringWrapper as W
from gui.helper import Configure, TempFile


class ExecutorThread(QThread):
    sig_finish_one = pyqtSignal()
    sig_all_down = pyqtSignal()
    sig_log = pyqtSignal(str, str)

    def __init__(self, parent, tests) -> None:
        super().__init__(parent)
        self.testcase_root = Path(Configure.get_config()["stage"][Configure.get_var("mode")]["testfile_path"])
        self.runtime_root = Path(TempFile.request_tempdir())
        self.result_root = Path("results") / time.strftime("%Y%m%d_%H%M%S", time.localtime())
        self.tests = list(map(lambda p: p.relative_to(self.testcase_root), tests))

        self.config_output = Configure.get_config()["stage"][Configure.get_var("mode")]["compiler_output_file"]
        self.config_answer = Configure.get_config()["stage"][Configure.get_var("mode")]["answer_filename"]

        # 'Part' is WA, in that this will not appear
        self.stat = {"AC": 0, "TLE": 0, "WA": 0, "RE": 0, "Mode": Configure.get_var("mode")}

    def run(self) -> None:
        self.result_root.mkdir(parents=True)
        for test in self.tests:
            self.sig_log.emit("进行测试: " + W.code(str(test)), "info")
            try:
                status, info = self.executor_java(test)  # TODO: Support more langs
            except Exception as e:
                self.sig_log.emit("遭遇了错误: " + W.code(repr(e)), "crit")
            else:
                if status == StatusCode.EXECUTE_RE:
                    self.sig_log.emit(f"RE> {info}", "warn")
                    self.stat["RE"] += 1
                elif status == StatusCode.EXECUTE_TLE:
                    self.sig_log.emit(f"TLE> {info}", "warn")
                    self.stat["TLE"] += 1
                elif status != StatusCode.JUDGE_AC:
                    self.sig_log.emit(f"WA> {info}", "warn")
                    self.stat["WA"] += 1
                else:
                    self.stat["AC"] += 1
            self.sig_finish_one.emit()
        self.sig_log.emit("== <b>AC</b>: " + str(self.stat["AC"]) + " <b>WA</b>: " + str(self.stat["WA"]) +
                          " <b>TLE</b>: " + str(self.stat["TLE"]) + " <b>RE</b>: " + str(self.stat["RE"]) +
                          " ==", "info")
        (self.result_root / "summary.txt").write_text(dumps(self.stat, ensure_ascii=True))
        self.sig_all_down.emit()

    def executor_java(self, test: Path) -> Tuple[StatusCode, str, str]:
        # region prepare dirsctory
        runtime_dir = self.runtime_root / test
        result_dir = self.result_root / test
        runtime_dir.parent.mkdir(parents=True, exist_ok=True)
        result_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(self.testcase_root / test), str(runtime_dir))
        shutil.copy(str(Configure.get_config()["lang"]["java"]["jar_path"]), str(runtime_dir / "Compiler.jar"))
        # endregion

        # region run & compare
        command = [
            "java", "-Dfile.encoding=UTF-8", "-jar", "Compiler.jar",
            Configure.get_config()["stage"][Configure.get_var("mode")]["args"]
        ]

        encoding_args = {"encoding": "utf-8", "errors": "replace"}

        try:
            ret_value = call(
                command,
                stdout=(result_dir / "stdout.txt").open("w", **encoding_args),
                stderr=(result_dir / "stderr.txt").open("w", **encoding_args),
                timeout=10,
                cwd=str(runtime_dir)
            )
            if 0 != ret_value:
                return (
                    StatusCode.EXECUTE_RE,
                    f"Return {ret_value} -> " +
                    W.code(
                        ((result_dir / "stderr.txt")
                           .read_text(**encoding_args) + "\n")  # Ensure at least one line
                           .splitlines()[0]
                           .replace("<", "&lt;")
                    )
                )

            s, d = LineCompare(str(test)).judge(
                runtime_dir / self.config_output,
                None,
                runtime_dir / self.config_answer,
            )
            (result_dir / "info.txt").write_text(s.name + "\n" + d["info"], **encoding_args)

            shutil.copy(str(runtime_dir / self.config_output), str(result_dir / self.config_output))
            shutil.copy(str(runtime_dir / self.config_answer), str(result_dir / self.config_answer))

            return s, d["info"].replace("<", "&lt;").replace("\n", " ")

        except TimeoutExpired:
            return StatusCode.EXECUTE_TLE, "Timeout of 10 s"
        # endregion
