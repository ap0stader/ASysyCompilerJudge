# This file cannot use the origin version in the tui version

from pathlib import Path
from json import loads
from typing import List

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


def __verify_helper(fn_prompt, keys: List[str]) -> bool:
    cfg = __config
    for key in keys[:-1]:
        cfg = cfg[key]
    if keys[-1] not in cfg:
        fn_prompt(" > ".join(keys))
        return False
    return True


def verify(fn_prompt) -> bool:
    ok_command = all(map(lambda x: __verify_helper(fn_prompt, x), (
        ["command"], ["command", "clang"],
        ["command", "llvm-link"], ["command", "lli"],
    )))

    ok_lang = all(map(lambda x: __verify_helper(fn_prompt, x), (
        # TODO: Support more languages
        ["lang"], ["lang", "programming language"], ["lang", "java", "jar_path"],
    )))

    ok_stage = all(map(lambda x: __verify_helper(fn_prompt, x), (
        ["stage"], ["stage", "lexical_analysis"], ["stage", "syntax_analysis"],
        ["stage", "semantic_analysis"], ["stage", "code_generation"],
    )))

    fn_stage_normal = lambda mid: all(map(lambda x: __verify_helper(
        fn_prompt, ["stage", mid, x]
    ), (
        "args", "testfile_path", "compiler_output_file", "error_filename",
        "sourcecode_filename", "answer_filename",
    )))

    ok_stage_normal = all(map(fn_stage_normal, (
        "lexical_analysis", "syntax_analysis", "semantic_analysis",
    )))

    ok_codegen_normal = all(map(lambda x: __verify_helper(fn_prompt, ["stage", "code_generation", x]), (
        "testfile_path", "sourcecode_filename", "input_filename",
        "answer_filename", "llvm", "mips", "mips_optimized",
    )))

    fn_codegen = lambda mid: all(map(lambda x: __verify_helper(
        fn_prompt, ["stage", "code_generation", mid, x]
    ), (
        "args", "compiler_output_file",
    )))

    ok_codegen = all(map(fn_codegen, (
        "llvm", "mips", "mips_optimized",
    )))

    return all((ok_command, ok_lang, ok_stage, ok_stage_normal, ok_codegen_normal, ok_codegen))
