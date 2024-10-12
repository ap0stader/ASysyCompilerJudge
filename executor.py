import json
import os
import time
from abc import ABC, abstractmethod

from pathlib import Path
from typing import Callable, List, Tuple, Dict, Union

from analyzer.common import Analyzer
from judge.common import Judge
from util.statuscode import StatusCode


class ExecutorUninitializedException(Exception):
    def __init__(self):
        super().__init__("Observers or execute of Executor has not been set")


class NoMatchJudgeTypeFoundException(Exception):
    def __init__(self, testcase_relative_path: str, typename: str):
        super().__init__("Type " + typename + " is not find in the judge_dict(testcase:"
                         + testcase_relative_path + ")")


class Executor:
    test_index: int

    def __init__(self, config):
        self.test_index = 0
        self.observers = []
        self.execute = None
        self.judge_config = config
        self.analyzers = []
        # 在分析器中注册各个评判器
        for task in config:
            for typename, triples in task["judge_dict"].items():
                for triple in triples:
                    for analyzer in triple["analyzers"]:
                        analyzer.register_origin(triple["judge"].name())
                        if analyzer not in self.analyzers:
                            self.analyzers.append(analyzer)

    def add_observer(self, observer):
        self.observers.append(observer)

    def set_execute(self, execute: Callable[[str, Path, Path], Tuple[StatusCode, str, str]]):
        self.execute = execute

    def observe(self, executor_start: Callable, started_observe_hook: Callable):
        if self.observers.__len__() == 0 or self.execute is None:
            raise ExecutorUninitializedException()

        for observer in self.observers:
            observer.start()
        if started_observe_hook is not None:
            started_observe_hook()

        # 测评第一次
        executor_start()

        try:
            while True:
                # TODO 控制台指令支持
                time.sleep(1)
        except KeyboardInterrupt:
            for observer in self.observers:
                observer.stop()

        for observer in self.observers:
            observer.join()

    def start(self,
              executor_start_hook: Callable,
              task_start_hook: Callable[[str], None],
              testcase_start_hook: Callable[[int, str], None],
              execute_status_hook: Callable[[int, str, StatusCode], None],
              judge_start_hook: Callable[[int, str, Judge], None],
              judge_status_hook: Callable[[int, str, Judge, StatusCode, dict], None],
              judge_end_hook: Callable[[int, str, Judge], None],
              summary_hook: Callable[[List[Analyzer]], None],
              executor_finish_hook: Callable[[str], None]):
        # 创建保存本次执行结果的文件夹
        now = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        result_dir = Path("./results/") / now
        result_dir.mkdir()
        # 摘要文件
        summary_path = result_dir / "summary.txt"
        # 准备分析器
        for analyzer in self.analyzers:
            analyzer.prepare()

        if executor_start_hook is not None:
            executor_start_hook()

        for task in self.judge_config:
            if task_start_hook is not None:
                task_start_hook(task["name"])
            self.judge(args=task["args"],
                       result_dir=result_dir,
                       testfile_path=task["testfile_path"],
                       config_filename=task["config_filename"],
                       sourcecode_filename=task["sourcecode_filename"],
                       input_filename=task["input_filename"],
                       answer_filename=task["answer_filename"],
                       judge_dict=task["judge_dict"],
                       testcase_start_hook=testcase_start_hook,
                       execute_status_hook=execute_status_hook,
                       judge_start_hook=judge_start_hook,
                       judge_status_hook=judge_status_hook,
                       judge_end_hook=judge_end_hook)

        if summary_hook is not None:
            summary_hook(self.analyzers)

        with open(summary_path, "w", encoding="utf-8") as summary:
            for analyzer in self.analyzers:
                summary.write(analyzer.summary())

        if executor_finish_hook is not None:
            executor_finish_hook(now)

    @staticmethod
    def walk_testcase_dir(testfile_path: Path,
                          config_filename: str,
                          sourcecode_filename: str, answer_filename: str,
                          input_filename: str):
        for root, dirs, files in os.walk(testfile_path):
            if (config_filename in files and
                    sourcecode_filename in files and
                    answer_filename in files and
                    (input_filename is None or input_filename in files)):
                yield Path(root)

    def judge(self, args: str, result_dir: Path, testfile_path: Path,
              config_filename: str, sourcecode_filename: str, input_filename: str, answer_filename: str,
              judge_dict: Dict[str, List[Dict[str, Union[str, Judge, Analyzer]]]],
              testcase_start_hook: Callable[[int, str], None],
              execute_status_hook: Callable[[int, str, StatusCode], None],
              judge_start_hook: Callable[[int, str, Judge], None],
              judge_status_hook: Callable[[int, str, Judge, StatusCode, dict], None],
              judge_end_hook: Callable[[int, str, Judge], None]
              ):
        # 通过便利找到所有的测试点
        for testcase_dir in self.walk_testcase_dir(testfile_path=testfile_path,
                                                   config_filename=config_filename,
                                                   sourcecode_filename=sourcecode_filename,
                                                   input_filename=input_filename,
                                                   answer_filename=answer_filename):
            # 测试点相对路径
            testcase_relative_path = testcase_dir.relative_to(testfile_path)
            # 配置文件
            config_path = testcase_dir / config_filename
            config = json.loads(config_path.read_text(encoding="utf-8"))
            testcase_typename = config["type"]
            if testcase_typename not in judge_dict.keys():
                raise NoMatchJudgeTypeFoundException(str(testcase_relative_path), testcase_typename)
            # 源代码文件
            sourcecode_path = testcase_dir / sourcecode_filename
            # 输入文件
            if input_filename is not None:
                input_path = testcase_dir / input_filename
            else:
                input_path = None
            # 答案文件
            answer_path = testcase_dir / answer_filename
            # 该测试点结果存放文件夹
            testcase_result_dir = result_dir / testcase_relative_path
            testcase_result_dir.mkdir(parents=True, exist_ok=True)
            # 评测信息文件
            info_path = testcase_result_dir / "info.txt"
            # 拉起一次测试
            with open(info_path, "w", encoding="utf-8") as info:
                # 测试数自增
                self.test_index += 1
                if testcase_start_hook is not None:
                    testcase_start_hook(self.test_index, str(testcase_relative_path))
                # 执行
                execute_status, execute_stdout, execute_stderr = self.execute(args=args,
                                                                              sourcecode_path=sourcecode_path,
                                                                              compiler_output_dir=testcase_result_dir)
                if execute_status_hook is not None:
                    execute_status_hook(self.test_index, str(testcase_relative_path), execute_status)

                if execute_status == StatusCode.EXECUTE_OK:
                    # 正常执行，进入评判
                    for triple in judge_dict[testcase_typename]:
                        compiler_output_filename = triple["compiler_output_filename"]
                        judge = triple["judge"]
                        analyzers = triple["analyzers"]
                        if judge_start_hook is not None:
                            judge_start_hook(self.test_index, str(testcase_relative_path), judge)
                        compiler_output_path = testcase_result_dir / compiler_output_filename

                        judge_status, judge_info_object = judge.judge(compiler_output_path=compiler_output_path,
                                                                      input_path=input_path,
                                                                      answer_path=answer_path)
                        if judge_status_hook is not None:
                            judge_status_hook(self.test_index, str(testcase_relative_path), judge,
                                              judge_status, judge_info_object)

                        if judge_status == StatusCode.JUDGE_AC:
                            info.writelines(
                                [">>> " + judge.name() + "\n>>> ACCEPTED\n", "\n"])
                        elif judge_status == StatusCode.JUDGE_WA:
                            info.writelines(
                                [">>> " + judge.name() + "\n>>> WRONG ANSWER\n", "\n"])
                        elif judge_status == StatusCode.JUDGE_TLE:
                            info.writelines(
                                [">>> " + judge.name() + "\n>>> COMPILER OK. BUT TIME LIMIT EXCEED WHEN JUDGE\n", "\n"])
                        elif judge_status == StatusCode.JUDGE_RE:
                            info.writelines(
                                [">>> " + judge.name() + "\n>>> COMPILER OK. BUT RUNTIME ERROR WHEN JUDGE\n", "\n"])
                        else:
                            info.writelines(
                                [">>> " + judge.name() + "\n>>> UNKNOWN ERROR WHEN JUDGE\n", "\n"])
                        info.writelines([">>> Judge Message\n", judge_info_object["info"], "\n"])
                        info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                        for analyzer in analyzers:
                            analyzer.analyze(judge_status, judge.name(), judge_info_object)
                        if judge_end_hook is not None:
                            judge_end_hook(self.test_index, str(testcase_relative_path), judge)
                elif execute_status == StatusCode.EXECUTE_TLE:
                    # 超时
                    info.writelines([">>> TIME LIMIT EXCEED\n", "\n"])
                    for triple in judge_dict[testcase_typename]:
                        for analyzer in triple["analyzers"]:
                            analyzer.analyze(StatusCode.EXECUTE_TLE, triple["judge"].name(), None)
                elif execute_status == StatusCode.EXECUTE_RE:
                    # 运行时错误
                    info.writelines([">>> RUNTIME ERROR\n", "\n"])
                    info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                    info.writelines([">>> Execute stderr\n", execute_stderr, "\n"])
                    for triple in judge_dict[testcase_typename]:
                        for analyzer in triple["analyzers"]:
                            analyzer.analyze(StatusCode.EXECUTE_RE, triple["judge"].name(), None)
                else:
                    # 未知情况
                    info.writelines([">>> UNKNOWN ERROR WHEN EXECUTE\n", "\n"])
                    info.writelines([">>> Execute stdout\n", execute_stdout, "\n"])
                    info.writelines([">>> Execute stderr\n", execute_stderr, "\n"])
                    for triple in judge_dict[testcase_typename]:
                        for analyzer in triple["analyzers"]:
                            analyzer.analyze(StatusCode.EXECUTE_UNKNOWN, triple["judge"].name(), None)


class ExecutorObserver(ABC):
    @abstractmethod
    def get_observer(self, executor: Executor):
        pass
