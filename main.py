from util import version

# 检查当前是否是最新版本
if not version.is_latest():
    raise Exception("You have update the sourcecode but have not update the environment!\n"
                    "Please run update.py first.")

from functools import partial

import configuration
import console

from executor import Executor
from util.termcolor import RESET, RED, INVERT

if __name__ == '__main__':
    print(">>> Parsing configurations...")
    # 解析配置文件
    CONFIG = configuration.get_config()

    print("[1] Lexical Analysis\n"
          "[2] Syntax Analysis\n"
          "[3] Semantic Analysis\n"
          "[C] Custom")
    stage_input = input("Please select the stage of your project [1-2 or C] ")
    match stage_input:
        case "1":
            # 词法分析
            mode = "lexical_analysis"
        case "2":
            # 语法分析
            mode = "syntax_analysis"
        case "3":
            # 语义分析
            mode = "semantic_analysis"
        # TODO 增加其他的阶段
        case "C":
            # 自定义评测
            mode = "custom"
        case _:
            raise KeyError("Invalid stage input!")
    # 获取执行配置和额外的监视器
    executor_config, additional_observer = configuration.get_executor_config(mode=mode)

    # 构建执行器
    executor = Executor(config=executor_config)
    for observer in additional_observer:
        executor.add_observer(observer.get_observer)
    print(">>> Executor is ready!\n")

    lang_input = CONFIG["lang"]["programming language"]
    match lang_input:
        case "java":
            jar_path = CONFIG["lang"]["java"]["jar_path"]
            print("- Programming language: " + RED + "Java" + RESET)
            print("- JAR file path: " + INVERT + str(jar_path) + RESET)
            from lang.java import Java

            start = input("Start observing JAR file? [Y/N] ")
            print()
            if start.upper() == "Y":
                lang = Java(jar_path=jar_path, detected_hook=console.java_detected_hook)
            else:
                print("Canceled.")
                exit(0)
        # TODO 增加其他开发语言
        case _:
            raise KeyError("Programming language " + lang_input + " is not supported")
    print(">>> Creating observer of " + lang.name() + "...")
    executor_start = partial(executor.start,
                             executor_start_hook=console.executor_start_hook,
                             task_start_hook=console.task_start_hook,
                             testcase_start_hook=console.testcase_start_hook,
                             execute_status_hook=console.execute_status_hook,
                             judge_start_hook=console.judge_start_hook,
                             judge_status_hook=console.judge_status_hook,
                             judge_end_hook=console.judge_end_hook,
                             summary_hook=console.summary_hook,
                             executor_finish_hook=console.executor_finish_hook)
    executor.add_observer(lang.get_observer(executor_start))
    executor.set_execute(lang.execute)
    executor.observe(executor_start=executor_start, started_observe_hook=console.started_observe_hook)

    print("\nGoodBye~")
