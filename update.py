# 更新工作环境
__CURRENT_VERSION = "1.3"

import os

print("=======   ASysyCompilerJudge Update   =======")

# 根据最新的requirements.txt安装依赖
print(">>>>> Update dependencies")
if os.system("pip install -r requirements.txt"):
    exit(1)

import sys
from pathlib import Path

from util.termcolor import RESET, RED, GREEN

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
        print("Your version is 1.0, which is too old. Please backup your data and run init.py!", file=sys.stderr)
        exit(1)
    case "1.1":
        pass
    case "1.2":
        pass
    case "1.3":
        print("You are up-to-date.")
    case _:
        print("Illegal version! Please backup your data and run init.py!", file=sys.stderr)
        exit(1)

with open("./VERSION", "w", encoding='utf-8') as version_file:
    version_file.write(__CURRENT_VERSION)

print(GREEN + "=======           Update End          =======" + RESET)
