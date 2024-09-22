# 更新工作环境
__CURRENT_VERSION = "1.2"

import os

print("=======   ASysyCompilerJudge Update   =======")

# 根据最新的requirements.txt安装依赖
print(">>>>> Update dependencies")
if os.system("pip install -r requirements.txt"):
    exit(1)

import shutil
import sys
from pathlib import Path

from util.termcolor import RESET, RED, GREEN, CYAN


# 升级custom_judge.py
def update_custom_judge():
    print(">>>>> Update custom_judge.py")
    custom_judge_input = input("A new version of custom_judge.py is prepared. Do you want to replace? [Y/N] ")
    if custom_judge_input.upper() == "Y":
        custom_judge_example_path = Path("./config_example/custom_judge.py")
        custom_judge_path = Path("./config/custom_judge.py")
        shutil.copy(custom_judge_example_path, custom_judge_path)
        print(GREEN + "New custom_judge.py copied." + RESET)
    else:
        print(CYAN + "Ignored." + RESET)


def update_gui():
    print("\n>>>>> Welcome to the GUI version!\n")
    print(f"You can run `{CYAN}winmain.py{RESET}` to launch the gui version, which supplies a fantasy wrap of the judge kernel")
    print(f"You can also run `{CYAN}main.py{RESET}` to use full as well as customed functions")


# 读取版本文件
version_path = Path("./VERSION")
if not version_path.is_file():
    print(RED + "VERSION file not found!\n"
                "This program is only for update.\n"
                "If you have not initialize the environment,\n"
                "please run init.py instead." + RESET)
    exit(1)

with open(version_path, "r", encoding='utf-8') as version_file:
    version = version_file.read().strip()

def write_version():
    with open("./VERSION", "w", encoding='utf-8') as f:
        f.write(__CURRENT_VERSION)


with open(version_path, "r", encoding='utf-8') as f:
    version = f.read().strip()
    match version:
        case "1.0":
            update_custom_judge()
            update_gui()
            write_version()
        case "1.1" | "1.2":
            update_gui()
            write_version()
        case "2.0":
            pass
        case _:
            print("Illegal version!", file=sys.stderr)
            exit(1)

print(GREEN + "=======           Update End          =======" + RESET)
