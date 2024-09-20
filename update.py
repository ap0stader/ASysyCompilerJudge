# 更新工作环境
import os
import shutil
from pathlib import Path

from util.termcolor import RESET, RED, GREEN, BRIGHT

print(BRIGHT + "=======   ASysyCompilerJudge Update   =======" + RESET)
print(RED + "This program is only for update.\n"
            "If you have not initialize the environment,\n"
            "please run init.py instead." + RESET)

sure = input(BRIGHT + "Are you sure? [Y/N]")

if sure == "Y" or sure == "y":
    # 根据最新的requirements.txt安装依赖
    print(">>>>>  Update dependencies")
    if os.system("pip install -r requirements.txt"):
        exit(1)
    # 升级custom_judge.py
    print(">>>>>  Update custom_judge.py")
    custom_judge_input = input("A new version of custom_judge.py is prepared. Do you want to continue? [Y/N] ")
    if custom_judge_input.upper() == "Y":
        custom_judge_example_path = Path("./config_example/custom_judge.py")
        custom_judge_path = Path("./config/custom_judge.py")
        shutil.copy(custom_judge_example_path, custom_judge_path)
        print(GREEN + "New custom_judge.py copied." + RESET)

    print(GREEN + "=======           Update End          =======" + RESET)

else:
    print("Canceled.")
