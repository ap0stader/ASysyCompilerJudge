# 初始化工作环境
import os.path
import shutil

from util import termcolor


# 删除之前的文件或文件夹，并根据情况决定决定是否创建新的文件夹
def process_folder(name: str, created: bool = True):
    if os.path.isdir("./" + name):
        shutil.rmtree("./" + name)
        print(termcolor.RED + "Previous " + name + " folder removed." + termcolor.RESET)
    elif os.path.isfile("./" + name):
        os.remove("./" + name)
        print(termcolor.RED + "Previous " + name + " file removed." + termcolor.RESET)
    if created:
        os.mkdir("./" + name)
        print(termcolor.GREEN + name + "/ folder created." + termcolor.RESET)


print(termcolor.BOLD + "=======   ASysyCompilerJudge Initialization   =======" + termcolor.RESET)
print(termcolor.RED + "=======               !ATTENTION!             =======\n"
                      "ALL files under [runtime/], [testfile/] and [config/]\n"
                      "                   WILL LOST FOREVER" + termcolor.RESET)

sure = input(termcolor.BOLD + "Are you sure? [Y/N]")

if sure == "Y" or sure == "y":
    print(termcolor.GREEN + "=======          Initialization Start         =======" + termcolor.RESET)

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
        print(termcolor.GREEN + "./testfile/" + folder + "/ folder created." + termcolor.RESET)
    # config文件夹
    print(">>>>>  Create config/")
    process_folder("config", False)
    shutil.copytree("./config_example/", "./config/", dirs_exist_ok=True)
    print(termcolor.GREEN + "config_example/ folder copied." + termcolor.RESET)

    print(termcolor.GREEN + "=======           Initialization End          =======" + termcolor.RESET)

    print(termcolor.ITALIC + "Please configure the judge.\n"
                             "See README.md for more details." + termcolor.RESET)

else:
    print("Canceled.")
