# 初始化工作环境
import os.path
import shutil

from util.termcolor import RESET, RED, GREEN, BOLD, ITALIC


# 删除之前的文件或文件夹，并根据情况决定决定是否创建新的文件夹
def process_folder(name: str, created: bool = True):
    if os.path.isdir("./" + name):
        shutil.rmtree("./" + name)
        print(RED + "Previous " + name + " folder removed." + RESET)
    elif os.path.isfile("./" + name):
        os.remove("./" + name)
        print(RED + "Previous " + name + " file removed." + RESET)
    if created:
        os.mkdir("./" + name)
        print(GREEN + name + "/ folder created." + RESET)


print(BOLD + "=======   ASysyCompilerJudge Initialization   =======" + RESET)
print(RED + "=======               !ATTENTION!             =======\n"
            "ALL files under [runtime/], [testfile/] and [config/]\n"
            "                   WILL LOST FOREVER" + RESET)

sure = input(BOLD + "Are you sure? [Y/N]")

if sure == "Y" or sure == "y":
    print(GREEN + "=======          Initialization Start         =======" + RESET)

    print(">>>>>  Install dependencies")
    if os.system("pip install -r requirements.txt"):
        exit(1)

    # runtime文件夹
    print(">>>>>  Create runtime/")
    process_folder("runtime")
    os.mkdir("./runtime/results")
    # testfile文件夹
    print(">>>>>  Create testfile/")
    process_folder("testfile")
    for folder in ("lexical_analysis", "syntax_analysis",
                   "error_handling", "code_generation"):
        os.mkdir("./testfile/" + folder)
        print(GREEN + "./testfile/" + folder + "/ folder created." + RESET)
    # config文件夹
    print(">>>>>  Create config/")
    process_folder("config", False)
    shutil.copytree("./config_example/", "./config/", dirs_exist_ok=True)
    print(GREEN + "config_example/ folder copied." + RESET)

    print(GREEN + "=======           Initialization End          =======" + RESET)

    print(ITALIC + "Please configure the judge.\n"
                   "See README.md for more details." + RESET)

else:
    print("Canceled.")
