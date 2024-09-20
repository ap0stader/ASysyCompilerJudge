# This file cannot use the origin version in the tui version

from pathlib import Path
from json import loads

from gui.helper.wrapper import StringWrapper as W

__Configure_Path = Path("config")
__Configure_Example_Path = Path("config_example")

__config = None
__files = ["lang", "command", "stage"]

def file_exist() -> bool:
    return __Configure_Path.is_dir() and all(
        map(lambda name: (__Configure_Path / f"{name}.json").is_file(), __files)
    )


def get_config(fn_prompt = None):
    global __config
    if __config is not None:
        return __config

    __config = {}

    for name in __files:
        if fn_prompt is not None:
            fn_prompt("读取配置: " + W.code(f"{name}.json") + " ...")
        __config[name] = loads((__Configure_Path / f"{name}.json").read_text(encoding='utf-8'))


def verify(fn_prompt) -> bool:
    # TODO: ...
    return True
