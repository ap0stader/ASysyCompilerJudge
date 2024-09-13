import json
from pathlib import Path

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


def get():
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
        except FileNotFoundError as e:
            print(f">>> {RED}Error: Cannot find the json file " +
                  f"`{CYAN}{openpath}{RED}`.{RESET}")
            exit(1)
        except json.JSONDecodeError:
            print(f">>> {RED}Error: Cannot parse the json file " +
                  f"`{CYAN}{openpath}{RED}`.{RESET}")
            exit(1)

    __config = config
    return config
