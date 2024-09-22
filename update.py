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

match version:
    case "1.0":
        update_custom_judge()
    case "1.1":
        pass
    case _:
        print("Illegal version!", file=sys.stderr)
        exit(1)

with open("./VERSION", "w", encoding='utf-8') as version_file:
    version_file.write(__CURRENT_VERSION)

print(GREEN + "=======           Update End          =======" + RESET)
