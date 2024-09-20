# 更新工作环境
import os

from util.termcolor import RESET, GREEN, BRIGHT

print(BRIGHT + "=======   ASysyCompilerJudge Update   =======" + RESET)

# 根据最新的requirements.txt安装依赖
print(">>>>>  Update dependencies")
if os.system("pip install -r requirements.txt"):
    exit(1)

print(GREEN + "=======           Update End          =======" + RESET)
