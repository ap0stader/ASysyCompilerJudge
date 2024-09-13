import os
import sys
import time

from pathlib import Path
from typing import Callable, List, Tuple

from judge.common import Judge
from util.statuscode import StatusCode
from util.termcolor import RED, RESET, BLUE, PURPLE, GREEN


class Executor:
    def __init__(self, config):
        self.observers = []
        self.execute = None
        self.args = config["args"]
        self.judge_type = config["judge_type"]
        self.judge_configs = config["judge_configs"]
        self.analyzer = config['analyzer']
        match self.judge_type:
            case "different":
                for judge_config in config["judge_configs"]:
                    self.analyzer.register_origin(judge_config["judge"].name())
            case "same":
                for judge_pair in config["judge_configs"]["judge_pairs"]:
                    self.analyzer.register_origin(judge_pair[1].name())
            case _:
                print("Wrong judge type", file=sys.stderr)
                exit(1)

    def add_observer(self, observer):
        self.observers.append(observer)

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
        print(">>>>> Starting Executor...")

        if self.judge_type == "different":
            self.different(result_files_path)
        elif self.judge_type == "same":
            self.same(result_files_path)

        self.analyzer.summary_print()
        with open(summary_path, "w") as summary:
            summary.write(self.analyzer.summary_save())
        print("Results folder: runtime/results/" + GREEN + now + RESET)
        print(">>> Finished judge! Continuing... ")

    def same(self, result_files_path: Path):
        # 确定测试文件各部分所在的文件夹
        sourcecode_files_path = self.judge_configs["testfile_path"] / self.judge_configs["sourcecode_prefix"]
        input_files_path = self.judge_configs["testfile_path"] / self.judge_configs["input_prefix"]
        answer_files_path = self.judge_configs["testfile_path"] / self.judge_configs["answer_prefix"]
        # 找到所有需要测试的源代码
        sourcecode_files = [f for f in os.listdir(sourcecode_files_path)
                            if (sourcecode_files_path / f).is_file()]
        sourcecode_files.sort()
        # 对每个文件进行测试
        for file_index in range(sourcecode_files.__len__()):
            # 源代码的名称
            sourcecode_name = sourcecode_files[file_index]
            # 确定各文件的路径
            sourcecode_path = sourcecode_files_path / sourcecode_name
            input_path = input_files_path / sourcecode_name.replace(self.judge_configs["sourcecode_prefix"],
                                                                    self.judge_configs["input_prefix"])
            answer_path = answer_files_path / sourcecode_name.replace(self.judge_configs["sourcecode_prefix"],
                                                                      self.judge_configs["answer_prefix"])
            # 确定输出文件的路径
            compiler_output_files_path = result_files_path / os.path.splitext(sourcecode_name)[0]
            info_path = result_files_path / sourcecode_name.replace(self.judge_configs["sourcecode_prefix"], "info")
            # 拉起一次测试
            self.test(file_index + 1,
                      info_path=info_path,
                      sourcecode_name=sourcecode_name,
                      sourcecode_path=sourcecode_path,
                      input_path=input_path,
                      answer_path=answer_path,
                      compiler_output_files_path=compiler_output_files_path,
                      judge_pairs=self.judge_configs["judge_pairs"])

    def different(self, result_files_path: Path):
        for judge_config in self.judge_configs:
            print(">>>>> Judge: " + judge_config["judge"].name())
            # 确定测试文件各部分所在的文件夹
            sourcecode_files_path = judge_config["testfile_path"] / judge_config["sourcecode_prefix"]
            input_files_path = judge_config["testfile_path"] / judge_config["input_prefix"]
            answer_files_path = judge_config["testfile_path"] / judge_config["answer_prefix"]
            result_judge_files_path = result_files_path / judge_config["judge"].name()
            result_judge_files_path.mkdir()
            # 找到所有需要测试的源代码
            sourcecode_files = [f for f in os.listdir(sourcecode_files_path)
                                if (sourcecode_files_path / f).is_file()]
            sourcecode_files.sort()
            # 对每个文件进行测试
            for file_index in range(sourcecode_files.__len__()):
                # 源代码的名称
                sourcecode_name = sourcecode_files[file_index]
                # 确定各文件的路径
                sourcecode_path = sourcecode_files_path / sourcecode_name
                input_path = input_files_path / sourcecode_name.replace(judge_config["sourcecode_prefix"],
                                                                        judge_config["input_prefix"])
                answer_path = answer_files_path / sourcecode_name.replace(judge_config["sourcecode_prefix"],
                                                                          judge_config["answer_prefix"])
                # 确定输出文件的路径
                compiler_output_files_path = result_judge_files_path / os.path.splitext(sourcecode_name)[0]
                info_path = result_judge_files_path / sourcecode_name.replace(judge_config["sourcecode_prefix"], "info")
                # 拉起一次测试
                self.test(file_index + 1,
                          info_path=info_path,
                          sourcecode_name=sourcecode_name,
                          sourcecode_path=sourcecode_path,
                          input_path=input_path,
                          answer_path=answer_path,
                          compiler_output_files_path=compiler_output_files_path,
                          judge_pairs=[(judge_config["compiler_output_file"], judge_config["judge"])])

    def test(self, test_index: int, info_path: Path, sourcecode_name: str, sourcecode_path: Path,
             input_path: Path, answer_path: Path, compiler_output_files_path: Path,
             judge_pairs: List[Tuple[str, Judge]]):
        with open(info_path, "w") as info:
            print("No." + str(test_index) + "\tSourcecode: " + sourcecode_name, end="\t", flush=True)
            execute_result, execute_stdout, execute_stderr = self.execute(self.args,
                                                                          sourcecode_path,
                                                                          compiler_output_files_path)
            if execute_result == StatusCode.EXECUTE_OK:
                # 正常执行，进入评判
                for compiler_output_file, judge in judge_pairs:
                    compiler_output_path = compiler_output_files_path / compiler_output_file
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
