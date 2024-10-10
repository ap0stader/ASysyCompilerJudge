# 更新工作环境
import os

print("=======   ASysyCompilerJudge Update   =======")

# 根据最新的requirements.txt安装依赖
print(">>>>> Update dependencies")
if os.system("pip install -r requirements.txt"):
    exit(1)

import sys

from util import version
from util.termcolor import RESET, RED, GREEN

match version.get_version():
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

version.write_version()

print(GREEN + "=======           Update End          =======" + RESET)
