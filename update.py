# 更新工作环境
import os

print("=======   ASysyCompilerJudge Update   =======")

# 根据最新的requirements.txt安装依赖
print(">>>>> Update dependencies")
if os.system("pip install -r requirements.txt"):
    exit(1)

import shutil
from pathlib import Path

from util import version
from util.termcolor import RESET, RED, GREEN


def update_config_stage():
    print(">>>>> Update config/stage.json")
    print("The config/stage.json will be created and " + RED + "the current one WILL BE DELETED." + RESET)
    print("Please backup it. If config/stage.json have not been modified, just continue.")
    sure = input("Continue? [Y/N] ")
    if sure == "Y" or sure == "y":
        origin = Path("./config/stage.json")
        new = Path("./config_example/stage.json")
        shutil.copy(new, origin)


def update_config_custom_judge():
    print(">>>>> Update config/custom_judge.py")
    print("The config/custom_judge.py will be created and " + RED + "the current one WILL BE DELETED." + RESET)
    print("Please backup it. If config/custom_judge.py have not been modified, just continue.")
    sure = input("Continue? [Y/N] ")
    if sure == "Y" or sure == "y":
        origin = Path("./config/custom_judge.py")
        new = Path("./config_example/custom_judge.py")
        shutil.copy(new, origin)


match version.get_version():
    case "1.0":
        raise Exception("Your version is 1.0, which is too old. Please backup your data and run init.py!")
    case "1.1":
        update_config_stage()
        update_config_custom_judge()
    case "1.2":
        update_config_stage()
        update_config_custom_judge()
    case "1.3":
        update_config_stage()
        update_config_custom_judge()
    case "2.0":
        print("You are up-to-date.")
    case _:
        raise Exception("Illegal version! Please backup your data and run init.py!")

version.write_version()

print(GREEN + "=======           Update End          =======" + RESET)
