import json
import sys
from pathlib import Path
from typing import Tuple, Dict, Any, List

from analyzer.statbyfile import StatByFile
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
            config[key] = json.loads(openpath.read_text())
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


def get_executor_config(mode: str) -> Tuple[Dict[str, Any], List[ExecutorObserver]]:
    match mode:
        case "lexical_analysis":
            name = "Lexical Analysis"
            return {
                "args": get_config()['stage'][mode]['args'],
                "judge_type": "different",
                "judge_configs": [
                    {
                        "compiler_output_file": get_config()['stage'][mode]['compiler_output_file'],
                        "judge": LineCompare(name),
                        "testfile_path": Path(get_config()['stage'][mode]['testfile_path']),
                        "sourcecode_filename": get_config()['stage'][mode]['sourcecode_filename'],
                        "input_filename": "",
                        "answer_filename": get_config()['stage'][mode]['answer_filename']
                    }
                ],
                "analyzer": StatByFile(name),
            }, []
        case "syntax_analysis":
            name = "Syntax Analysis"
            return {
                "args": get_config()['stage'][mode]['args'],
                "judge_type": "different",
                "judge_configs": [
                    {
                        "compiler_output_file": get_config()['stage'][mode]['compiler_output_file'],
                        "judge": LineCompare(name),
                        "testfile_path": Path(get_config()['stage'][mode]['testfile_path']),
                        "sourcecode_filename": get_config()['stage'][mode]['sourcecode_filename'],
                        "input_filename": "",
                        "answer_filename": get_config()['stage'][mode]['answer_filename']
                    }
                ],
                "analyzer": StatByFile(name),
            }, []
        case "custom":
            import config.custom_judge as custom
            return custom.get()
        case _:
            print("When get_executor_config(), got wrong mode", file=sys.stderr)
            exit(1)
