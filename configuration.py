import json
from pathlib import Path
from typing import Tuple, Dict, Any, List

from analyzer.statstatus import StatStatus
from executor import ExecutorObserver
from judge.linecompare import LineCompare

__config = None

__CONFIG_ITEMS = [
    # 名称、文件名、是否可以使用example文件
    ("lang", "lang.json"),
    ("stage", "stage.json"),
    ("command", "command.json"),
]

__CONFIG_PATH = Path("./config")


# 解析配置文件
def get_config():
    global __config
    if __config is not None:
        return __config

    config = {}

    for key, filename in __CONFIG_ITEMS:
        openpath = (__CONFIG_PATH / filename)
        config[key] = json.loads(openpath.read_text(encoding="utf-8"))

    __config = config
    return config


class ModeWrongException(Exception):
    def __init__(self):
        super().__init__("When get_executor_config(), got wrong mode.")


# 根据配置文件和指定模式返回执行配置和额外的监视器
def get_executor_config(mode: str) -> Tuple[List[Dict[str, Any]], List[ExecutorObserver]]:
    if mode == "custom":
        import config.custom_judge as custom
        return custom.get()
    elif mode == "lexical_analysis":
        public_analyzer = StatStatus("Lexical Analysis")
        return [{
            "name": "Lexical Analysis",
            "args": get_config()["stage"][mode]["args"],
            "testfile_path": Path(get_config()["stage"][mode]["testfile_path"]),
            "config_filename": "config.json",
            "sourcecode_filename": "testfile.txt",
            "input_filename": None,
            "answer_filename": "ans.txt",
            "judge_dict": {
                "lexer": [{
                    "compiler_output_filename": "lexer.txt",
                    "judge": LineCompare("Lexical Analysis (Lexer)"),
                    "analyzers": [public_analyzer]
                }],
                "error": [{
                    "compiler_output_filename": "error.txt",
                    "judge": LineCompare("Lexical Analysis (Error)"),
                    "analyzers": [public_analyzer]
                }],
            },
        }], []
    elif mode == "syntax_analysis":
        public_analyzer = StatStatus("Syntax Analysis")
        return [{
            "name": "Syntax Analysis",
            "args": get_config()["stage"][mode]["args"],
            "testfile_path": Path(get_config()["stage"][mode]["testfile_path"]),
            "config_filename": "config.json",
            "sourcecode_filename": "testfile.txt",
            "input_filename": None,
            "answer_filename": "ans.txt",
            "judge_dict": {
                "parser": [{
                    "compiler_output_filename": "parser.txt",
                    "judge": LineCompare("Syntax Analysis (Parser)"),
                    "analyzers": [public_analyzer]
                }],
                "error": [{
                    "compiler_output_filename": "error.txt",
                    "judge": LineCompare("Syntax Analysis (Error)"),
                    "analyzers": [public_analyzer]
                }],
            },
        }], []
    elif mode == "semantic_analysis":
        public_analyzer = StatStatus("Semantic Analysis")
        return [{
            "name": "Semantic Analysis",
            "args": get_config()["stage"][mode]["args"],
            "testfile_path": Path(get_config()["stage"][mode]["testfile_path"]),
            "config_filename": "config.json",
            "sourcecode_filename": "testfile.txt",
            "input_filename": None,
            "answer_filename": "ans.txt",
            "judge_dict": {
                "symbol": [{
                    "compiler_output_filename": "symbol.txt",
                    "judge": LineCompare("Semantic Analysis (Symbol)"),
                    "analyzers": [public_analyzer]
                }],
                "error": [{
                    "compiler_output_filename": "error.txt",
                    "judge": LineCompare("Semantic Analysis (Error)"),
                    "analyzers": [public_analyzer]
                }],
            },
        }], []
    else:
        raise ModeWrongException()
