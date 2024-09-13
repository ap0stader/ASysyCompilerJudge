import os
import sys
import time
from pathlib import Path
from typing import Callable, Tuple, List

from watchdog.observers import Observer

from analyzer.common import Analyzer
from judge.common import Judge
from util.statuscode import StatusCode
from util.termcolor import RED, RESET, BLUE, PURPLE, GREEN


class Executor:
    def __init__(self, args: str, testfile_path: Path,
                 judge_triple: List[List[str], List[Judge], Analyzer],
                 sourcecode_prefix: str, input_prefix: str, answer_prefix: str):
        self.compiler_observer = None
        self.execute = None

        self.args = args
        self.testfile_path = testfile_path

        self.judge_compiler_output_files = judge_triple[0]
        self.judges = judge_triple[1]
        for i in range(self.judges.__len__()):
            self.judges[i].init()
        self.analyzer = judge_triple[2]

        self.sourcecode_prefix = sourcecode_prefix
        self.input_prefix = input_prefix
        self.answer_prefix = answer_prefix

    def set_compiler_observer(self, compiler_observer: Observer):
        self.compiler_observer = compiler_observer

    def set_execute(self, execute: Callable[[str, str, str], Tuple[StatusCode, str, str]]):
        self.execute = execute

    def observe(self):
        if self.compiler_observer is None or self.execute is None:
            print("Compiler Observer or Execute of Executor has not been set", file=sys.stderr)
            exit(1)

        # TODO 测试文件的观察者
        # print(">>> Creating Testfile Observer...")

        self.compiler_observer.start()
        print(">>> Observer Started!")
        print(">>> Press Ctrl+C to exit.")

        try:
            while True:
                # TODO 控制台指令支持
                time.sleep(1)
        except KeyboardInterrupt:
            self.compiler_observer.stop()

        self.compiler_observer.join()

    def start(self):
        # 确定测试文件各部分所在的文件夹
        sourcecode_files_path = self.testfile_path / self.sourcecode_prefix
        input_files_path = self.testfile_path / self.input_prefix
        answer_files_path = self.testfile_path / self.answer_prefix
        # 保存本次执行结果的文件夹
        now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        result_files_path = Path("./results/") / now
        result_files_path.mkdir()
        summary_path = result_files_path / "summary.txt"
        # 准备分析器
        self.analyzer.prepare()
        # 找到所有需要测试的源代码
        sourcecode_files = [f for f in os.listdir(sourcecode_files_path)
                            if (sourcecode_files_path / f).is_file()]
        sourcecode_files.sort()
        # 对每个文件纪进行测试
        print(">>>>> Starting Executor...")
        for file_index in range(1, sourcecode_files.__len__() + 1):
            # 源代码的名称
            sourcecode_name = sourcecode_files[file_index]
            # 确定各文件的路径
            sourcecode_path = sourcecode_files_path / sourcecode_name
            input_path = input_files_path / sourcecode_name.replace(self.sourcecode_prefix, self.input_prefix)
            answer_path = answer_files_path / sourcecode_name.replace(self.sourcecode_prefix, self.answer_prefix)
            # 确定输出文件的路径
            compiler_output_files_path = result_files_path / os.path.splitext(sourcecode_name)[0]
            info_path = result_files_path / sourcecode_name.replace(self.sourcecode_prefix, "info")
            with open(info_path, "w") as info:
                print("Test  " + str(file_index) + "\tSourcecode: " + sourcecode_name, end="\t", flush=True)
                (execute_result, execute_stdout, execute_stderr) = self.execute(self.args,
                                                                                sourcecode_path,
                                                                                compiler_output_files_path)
                if execute_result == StatusCode.EXECUTE_OK:
                    # 正常执行，进入评判
                    for compiler_output_file, judge in zip(self.judge_compiler_output_files, self.judges):
                        compiler_output_path = compiler_output_files_path / compiler_output_file
                        judge_result, judge_info_object = judge.judge(compiler_output_path, input_path, answer_path)

                        if judge_result == StatusCode.JUDGE_AC:
                            print(judge.name() + "=>" + GREEN + "AC" + RESET +
                                  "(" + judge_info_object["info"] + ")", end="\t")
                            info.writelines([">>> ACCEPTED\n", "\n"])
                            info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                            info.writelines([">>> Judge Message\n", judge_info_object["info"], "\n"])
                        elif judge_result == StatusCode.JUDGE_WA:
                            print(judge.name() + "=>" + RED + "WA" + RESET, end="\t")
                            info.writelines([">>> WRONG ANSWER\n", "\n"])
                            info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                            info.writelines([">>> Judge Message\n", judge_info_object["info"], "\n"])
                        else:
                            print(judge.name() + "=>" + "UNKNOWN", end="\t")
                            info.writelines([">>> UNKNOWN ERROR WHEN JUDGE\n", "\n"])
                            info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                            info.writelines([">>> Judge Message\n", judge_info_object["info"], "\n"])
                        print()
                elif execute_result == StatusCode.EXECUTE_TLE:
                    # 超时
                    print(BLUE + "TLE" + RESET)
                    info.writelines([">>> TIME LIMIT EXCEED\n", "\n"])
                    self.analyzer.add(StatusCode.EXECUTE_TLE, None, None)
                elif execute_result == StatusCode.EXECUTE_RE:
                    # 运行时错误
                    print(PURPLE + "RE" + RESET)
                    info.writelines([">>> RUNTIME ERROR\n", "\n"])
                    info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                    info.writelines([">>> Execute stderr\n", execute_stderr, "\n"])
                    self.analyzer.add(StatusCode.EXECUTE_RE, None, None)
                else:
                    # 未知情况
                    print("UNKNOWN")
                    info.writelines([">>> UNKNOWN ERROR WHEN EXECUTE\n", "\n"])
                    info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                    info.writelines([">>> Execute stderr\n", execute_stderr, "\n"])
                    self.analyzer.add(StatusCode.EXECUTE_UNKNOWN, None, None)

        self.analyzer.summary_print()
        with open(summary_path, "w") as summary:
            summary.write(self.analyzer.summary_save())
        print("Results folder: runtime/results/" + GREEN + now + RESET)
        print(">>> Finished judge! Continuing... ")
