# 初始化工作环境
import os
import shutil
import sys
from pathlib import Path

from util.termcolor import RESET, RED, GREEN, BRIGHT, ITALIC


# 删除之前的文件或文件夹，并根据情况决定决定是否创建新的文件夹
def process_folder(path: Path, created: bool = True):
    if path.is_dir():
        shutil.rmtree(path)
        print(RED + "Previous " + str(path) + " folder removed." + RESET)
    elif path.is_file():
        path.unlink()
        print(RED + "Previous " + str(path) + " file removed." + RESET)
    if created:
        path.mkdir()
        print(GREEN + str(path) + " folder created." + RESET)


print(BRIGHT + "=======   ASysyCompilerJudge Initialization   =======" + RESET)
print(RED + "=======               !ATTENTION!             =======\n"
            "ALL files under [runtime/], [testfile/] and [config/]\n"
            "                   WILL LOST FOREVER" + RESET)

sure = input(BRIGHT + "Are you sure? [Y/N]")

if sure == "Y" or sure == "y":
    print(GREEN + "=======          Initialization Start         =======" + RESET)

    print(">>>>>  Install dependencies")
    if os.system("pip install -r requirements.txt"):
        exit(1)
    # runtime文件夹
    print(">>>>>  Create runtime/")
    runtime = Path("./runtime")
    process_folder(runtime)
    # results文件夹
    print(">>>>>  Create results/")
    results = Path("./results")
    if results.is_file():
        print("Previous " + str(results) + " is a file. Please backup and delete it.", file=sys.stderr)
        exit(1)
    # 如果已经有results文件夹，不删除其内容
    results.mkdir(exist_ok=True)
    print(GREEN + str(results) + " folder created." + RESET)
    # testfile文件夹
    print(">>>>>  Create testfile/")
    testfile = Path("./testfile")
    process_folder(testfile)
    for folder in ("lexical_analysis", "syntax_analysis",
                   "semantic_analysis", "code_generation"):
        (testfile / folder).mkdir()
        print(GREEN + str(testfile / folder) + " folder created." + RESET)
    # config文件夹
    print(">>>>>  Create config/")
    config = Path("./config")
    config_example = Path("./config_example")
    process_folder(config, False)
    # 将示例配置文件复制形成configw文件夹
    shutil.copytree(config_example, config)
    print(GREEN + str(config_example) + " folder copied." + RESET)

    print(GREEN + "=======           Initialization End          =======" + RESET)
    print(ITALIC + "Please configure the judge.\n"
                   "See README.md for more details." + RESET)

else:
    print("Canceled.")
