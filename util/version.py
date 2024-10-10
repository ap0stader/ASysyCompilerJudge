from pathlib import Path

from util.termcolor import RESET, RED

# 当前版本
CURRENT_VERSION = "1.3"


# 获取版本
def get_version() -> str:
    version_path = Path("./VERSION")
    if not version_path.is_file():
        print(RED + "VERSION file not found!\n"
                    "If you have not initialize the environment,\n"
                    "please run init.py first." + RESET)
        exit(1)
    with open(version_path, "r", encoding='utf-8') as version_file:
        version = version_file.read().strip()
        return version


# 判断是否是最新版
def is_latest():
    return get_version() == CURRENT_VERSION


# 写入版本
def write_version(version: str = CURRENT_VERSION):
    with open("./VERSION", "w", encoding='utf-8') as version_file:
        version_file.write(version)
