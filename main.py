import sys
from pathlib import Path

import configuration
import triple

from executor import Executor
from util.termcolor import RESET, RED, GREEN, INVERSE

if __name__ == '__main__':
    print(">>> Parsing configurations...")
    CONFIG = configuration.get()

    print("[1] Lexical Analysis\n"
          "[2] Syntax Analysis")
    stage = input("Please select the stage of your project [1-2] ")
    # 配置文件模式
    match stage:
        case "1":
            # 词法分析
            mode = "lexical_analysis"
            judge_triple = triple.get(mode=mode)
            args = CONFIG['stage']["lexical_analysis"]['args']
        case "2":
            # 语法分析
            mode = "syntax_analysis"
            judge_triple = triple.get(mode=mode)
            args = CONFIG['stage']["syntax_analysis"]['args']
        # TODO 增加其他的阶段
        case _:
            print("Invalid input", file=sys.stderr)
            exit(1)
    # 读取配置文件内容
    testfile_dir = Path(CONFIG['stage'][mode]['testfile_path'])
    sourcecode_prefix = CONFIG['stage'][mode]['sourcecode_prefix']
    input_prefix = ""
    if 'input_prefix' in CONFIG['stage'][mode]:
        input_prefix = CONFIG['stage'][mode]['input_prefix']
    answer_prefix = CONFIG['stage'][mode]['answer_prefix']
    # TODO 增加自定义评测模式
    # 构建执行器
    executor = Executor(args=args, testfile_path=testfile_dir, judge_triple=judge_triple,
                        sourcecode_prefix=sourcecode_prefix, input_prefix=input_prefix, answer_prefix=answer_prefix)
    print(">>> Executor is ready!")
    print(">>> Arguments: " + GREEN + args + RESET)
    print(">>> Testfile Directory: " + GREEN + str(testfile_dir) + RESET)
    print()

    lang = CONFIG['lang']['programming language']
    match lang:
        case 'java':
            jar_path = CONFIG['lang']['java']['jar_path']
            print("- Programming language: " + RED + "Java" + RESET)
            print("- JAR file path: " + INVERSE + str(jar_path) + RESET)
            from lang import java

            start = input("Start observing JAR file? [Y/N] ")
            print()
            if start.upper() == "Y":
                executor.set_compiler_observer(java.get_observer(executor=executor, jar_path=jar_path))
                executor.set_execute(java.execute)
        # TODO 增加其他开发语言
        case _:
            print("Programming language " + lang + " is not supported", file=sys.stderr)
            exit(1)
    executor.observe()

    print("\nGoodBye~")
