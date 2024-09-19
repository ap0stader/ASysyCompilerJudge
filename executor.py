import os
import sys
import time
from abc import ABC, abstractmethod

from pathlib import Path
from typing import Callable, List, Tuple

from judge.common import Judge
from util.statuscode import StatusCode
from util.termcolor import RED, RESET, BLUE, PURPLE, GREEN


def walk_testcase_dir(testfile_path: Path,
                      sourcecode_filename: str, input_filename: str, answer_filename: str):
    for root, dirs, files in os.walk(testfile_path):
        if (sourcecode_filename in files and answer_filename in files and
                (input_filename is None or input_filename in files)):
            yield Path(root)


class Executor:
    test_index: int

    def __init__(self, config):
        self.test_index = 0
        self.observers = []
        self.execute = None
        self.args = config["args"]
        self.judge_type = config["judge_type"]
        self.judge_configs = config["judge_configs"]
        self.analyzer = config['analyzer']
        match self.judge_type:
            case "multiple":
                for judge_config in config["judge_configs"]:
                    self.analyzer.register_origin(judge_config["judge"].name())
            case "single":
                for judge_pair in config["judge_configs"]["judge_pairs"]:
                    self.analyzer.register_origin(judge_pair[1].name())
            case _:
                print("Wrong judge type", file=sys.stderr)
                exit(1)

    def add_observer(self, get_observer: Callable):
        self.observers.append(get_observer(self))

    def set_execute(self, execute: Callable[[str, str, str], Tuple[StatusCode, str, str]]):
        self.execute = execute

    def observe(self):
        if self.observers.__len__() == 0 or self.execute is None:
            print("Observer or Execute of Executor has not been set", file=sys.stderr)
            exit(1)

        for observer in self.observers:
            observer.start()
        print(">>> All Observer Started!")
        print(">>> Press Ctrl+C to exit.")

        # 测评一次
        self.start()

        try:
            while True:
                # TODO 控制台指令支持
                time.sleep(1)
        except KeyboardInterrupt:
            for observer in self.observers:
                observer.stop()

        for observer in self.observers:
            observer.join()

    def start(self):
        # 保存本次执行结果的文件夹
        now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        result_files_path = Path("./results/") / now
        result_files_path.mkdir()
        summary_path = result_files_path / "summary.txt"
        # 准备分析器
        self.analyzer.prepare()
        print(">>> Starting Executor...")

        if self.judge_type == "multiple":
            for judge_config in self.judge_configs:
                print(">>> Judge: " + judge_config["judge"].name())
                self.judge(result_files_path=result_files_path,
                           testfile_path=judge_config["testfile_path"],
                           sourcecode_filename=judge_config["sourcecode_filename"],
                           input_filename=judge_config["input_filename"],
                           answer_filename=judge_config["answer_filename"],
                           judge_pairs=[(judge_config["compiler_output_file"], judge_config["judge"])])
        elif self.judge_type == "single":
            self.judge(result_files_path=result_files_path,
                       testfile_path=self.judge_configs["testfile_path"],
                       sourcecode_filename=self.judge_configs["sourcecode_filename"],
                       input_filename=self.judge_configs["input_filename"],
                       answer_filename=self.judge_configs["answer_filename"],
                       judge_pairs=self.judge_configs["judge_pairs"])

        self.analyzer.summary_print()
        with open(summary_path, "w") as summary:
            summary.write(self.analyzer.summary_save())
        print("Results folder: runtime/results/" + GREEN + now + RESET)
        print(">>> Finished judge! Continuing... ")

    def judge(self, result_files_path: Path, testfile_path: Path,
              sourcecode_filename: str, input_filename: str, answer_filename: str,
              judge_pairs: List[Tuple[str, Judge]]):
        for testcase_dir in walk_testcase_dir(testfile_path=testfile_path,
                                              sourcecode_filename=sourcecode_filename,
                                              input_filename=input_filename,
                                              answer_filename=answer_filename):
            # 确定测试文件各部分所在的路径
            sourcecode_path = testcase_dir / sourcecode_filename
            if input_filename is not None:
                input_path = testcase_dir / input_filename
            else:
                input_path = None
            answer_path = testcase_dir / answer_filename
            # 确定结果文件所在的位置
            testcase_relative_path = testcase_dir.relative_to(testfile_path)
            testcase_result_files_path = result_files_path / testcase_relative_path
            testcase_result_files_path.mkdir(parents=True, exist_ok=True)
            info_path = testcase_result_files_path / "info.txt"
            # 拉起一次测试
            with open(info_path, "w") as info:
                self.test_index += 1
                print("No." + str(self.test_index) + "\tSourcecode: " + str(testcase_relative_path),
                      end="\t", flush=True)
                execute_result, execute_stdout, execute_stderr = self.execute(self.args,
                                                                              sourcecode_path,
                                                                              testcase_result_files_path)
                if execute_result == StatusCode.EXECUTE_OK:
                    # 正常执行，进入评判
                    for compiler_output_file, judge in judge_pairs:
                        compiler_output_path = testcase_result_files_path / compiler_output_file
                        judge_statuscode, judge_info_object = judge.judge(compiler_output_path,
                                                                          input_path,
                                                                          answer_path)
                        self.analyzer.analyze(judge_statuscode, judge.name(), judge_info_object)
                        if judge_statuscode == StatusCode.JUDGE_AC:
                            print(judge.name() + "=>" + GREEN + "AC" + RESET, end="")
                            if judge_info_object["info"] != "":
                                print("(" + judge_info_object["info"] + ")", end="\t")
                            else:
                                print("", end="\t")
                            info.writelines([">>> " + judge.name() + "\n>>> ACCEPTED\n", "\n"])
                            info.writelines([">>> Judge Message\n", judge_info_object["info"], "\n"])
                        elif judge_statuscode == StatusCode.JUDGE_WA:
                            print(judge.name() + "=>" + RED + "WA" + RESET, end="\t")
                            info.writelines([">>> " + judge.name() + "\n>>> WRONG ANSWER\n", "\n"])
                            info.writelines([">>> Judge Message\n", judge_info_object["info"], "\n"])
                        else:
                            print(judge.name() + "=>" + "UNKNOWN", end="\t")
                            info.writelines([">>> " + judge.name() + "\n>>> UNKNOWN ERROR WHEN JUDGE\n", "\n"])
                            info.writelines([">>> Judge Message\n", judge_info_object["info"], "\n"])
                    print()
                    info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                elif execute_result == StatusCode.EXECUTE_TLE:
                    # 超时
                    print(BLUE + "TLE" + RESET)
                    info.writelines([">>> TIME LIMIT EXCEED\n", "\n"])
                    self.analyzer.analyze(StatusCode.EXECUTE_TLE, None, None)
                elif execute_result == StatusCode.EXECUTE_RE:
                    # 运行时错误
                    print(PURPLE + "RE" + RESET)
                    info.writelines([">>> RUNTIME ERROR\n", "\n"])
                    info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                    info.writelines([">>> Execute stderr\n", execute_stderr, "\n"])
                    self.analyzer.analyze(StatusCode.EXECUTE_RE, None, None)
                else:
                    # 未知情况
                    print("UNKNOWN")
                    info.writelines([">>> UNKNOWN ERROR WHEN EXECUTE\n", "\n"])
                    info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                    info.writelines([">>> Execute stderr\n", execute_stderr, "\n"])
                    self.analyzer.analyze(StatusCode.EXECUTE_UNKNOWN, None, None)


class ExecutorObserver(ABC):
    @abstractmethod
    def get_observer(self, executor: Executor):
        pass
