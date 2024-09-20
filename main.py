import sys

import configuration

from executor import Executor
from util.termcolor import RESET, RED, INVERT

if __name__ == '__main__':
    print(">>> Parsing configurations...")
    # 解析配置文件
    CONFIG = configuration.get_config()

    print("[1] Lexical Analysis\n"
          "[2] Syntax Analysis\n"
          "[C] Custom")
    stage_input = input("Please select the stage of your project [1-2 or C] ")
    match stage_input:
        case "1":
            # 词法分析
            mode = "lexical_analysis"
        case "2":
            # 语法分析
            mode = "syntax_analysis"
        # TODO 增加其他的阶段
        case "C":
            # 自定义评测
            mode = "custom"
        case _:
            print("Invalid input", file=sys.stderr)
            exit(1)
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
                lang = Java(jar_path=jar_path)
            else:
                print("Canceled.")
                exit(1)
        # TODO 增加其他开发语言
        case _:
            print("Programming language " + lang_input + " is not supported", file=sys.stderr)
            exit(1)
    executor.add_observer(lang.get_observer)
    executor.set_execute(lang.execute)
    executor.observe()

    print("\nGoodBye~")
