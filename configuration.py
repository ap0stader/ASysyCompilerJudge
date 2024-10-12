import json
import sys
from pathlib import Path
from typing import Tuple, Dict, Any, List

from analyzer.statstatus import StatStatus
from executor import ExecutorObserver
from judge.linecompare import LineCompare
from util.termcolor import RESET, RED, YELLOW, CYAN

__config = None

__CONFIG_ITEMS = [
    # 名称、文件名、是否可以使用example文件
    ("lang", "lang.json", False),
    ("stage", "stage.json", True),
    ("command", "command.json", True),
]

__CONFIG_PATH = Path("./config")
__EXAMPLE_PATH = Path("./config_example")


# 解析配置文件
def get_config():
    global __config
    if __config is not None:
        return __config

    config = {}

    for key, filename, rollback in __CONFIG_ITEMS:
        openpath = (__CONFIG_PATH / filename)
        if rollback and (not openpath.is_file()):
            print(f">>> {YELLOW}Warning: Cannot find the json file " +
                  f"`{CYAN}{openpath}{YELLOW}` Use example file instead.{RESET}")
            openpath = (__EXAMPLE_PATH / filename)
        try:
            config[key] = json.loads(openpath.read_text(encoding="utf-8"))
        except FileNotFoundError:
            print(f">>> {RED}Error: Cannot find the json file " +
                  f"`{CYAN}{openpath}{RED}`.{RESET}")
            exit(1)
        except json.JSONDecodeError:
            print(f">>> {RED}Error: Cannot parse the json file " +
                  f"`{CYAN}{openpath}{RED}`.{RESET}")
            exit(1)

    __config = config
    return config


# 根据配置文件和指定模式返回执行配置和额外的监视器
def get_executor_config(mode: str) -> Tuple[List[Dict[str, Any]], List[ExecutorObserver]]:
    if mode == "custom":
        import config.custom_judge as custom
        return custom.get()
    elif mode == "lexical_analysis":
        public_analyzer = StatStatus("Lexical Analysis")
        return [{
            "args": get_config()["stage"][mode]["args"],
            "testfile_path": Path(get_config()["stage"][mode]["testfile_path"]),
            "sourcecode_filename": "testfile.txt",
            "input_filename": None,
            "answer_filename": "ans.txt",
            "judge_configs": {
                "lexer": [{
                    "compiler_output_filename": "lexer.txt",
                    "judge": LineCompare("Lexical Analysis (Lexer)"),
                    "analyzer": public_analyzer
                }],
                "error": [{
                    "compiler_output_filename": "error.txt",
                    "judge": LineCompare("Lexical Analysis (Error)"),
                    "analyzer": public_analyzer
                }],
            },
        }], []
    elif mode == "syntax_analysis":
        public_analyzer = StatStatus("Syntax Analysis")
        return [{
            "args": get_config()["stage"][mode]["args"],
            "testfile_path": Path(get_config()["stage"][mode]["testfile_path"]),
            "sourcecode_filename": "testfile.txt",
            "input_filename": None,
            "answer_filename": "ans.txt",
            "judge_configs": {
                "lexer": [{
                    "compiler_output_filename": "parser.txt",
                    "judge": LineCompare("Syntax Analysis (Parser)"),
                    "analyzer": public_analyzer
                }],
                "error": [{
                    "compiler_output_filename": "error.txt",
                    "judge": LineCompare("Syntax Analysis (Error)"),
                    "analyzer": public_analyzer
                }],
            },
        }], []
    elif mode == "semantic_analysis":
        public_analyzer = StatStatus("Semantic Analysis")
        return [{
            "args": get_config()["stage"][mode]["args"],
            "testfile_path": Path(get_config()["stage"][mode]["testfile_path"]),
            "sourcecode_filename": "testfile.txt",
            "input_filename": None,
            "answer_filename": "ans.txt",
            "judge_configs": {
                "symbol": [{
                    "compiler_output_filename": "symbol.txt",
                    "judge": LineCompare("Semantic Analysis (Symbol)"),
                    "analyzer": public_analyzer
                }],
                "error": [{
                    "compiler_output_filename": "error.txt",
                    "judge": LineCompare("Semantic Analysis (Error)"),
                    "analyzer": public_analyzer
                }],
            },
        }], []
    else:
        print("When get_executor_config(), got wrong mode", file=sys.stderr)
        exit(1)
