import os
import shutil
from pathlib import Path
from subprocess import Popen, PIPE, TimeoutExpired

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from executor import Executor
from util.statuscode import StatusCode
from util.termcolor import RESET, INVERSE

__TEMP_BASE = Path("./runtime/java/")
__TEMP_JAR = __TEMP_BASE / "Compiler.jar"
__TEMP_WORKDIR = __TEMP_BASE / "workdir"
__TEMP_SOURCECODE = __TEMP_WORKDIR / "testfile.txt"


class ModifiedHandler(FileSystemEventHandler):
    def __init__(self, executor: Executor, jar_name: str):
        self.executor = executor
        self.jar_name = jar_name

    def on_created(self, event):
        if not event.is_directory and os.path.basename(event.src_path) == self.jar_name:
            print("New " + INVERSE + self.jar_name + RESET + " has been detected", end="")
            shutil.copy(event.src_path, __TEMP_JAR)
            print(" and copied.")
            self.executor.start()


def get_observer(executor: Executor, jar_path: str):
    print(">>> Creating Java Observer...")
    # 创建Java开发语言的文件夹
    __TEMP_BASE.mkdir(exist_ok=True)
    # 分析JAR文件所在文件的目录和JAR文件名
    jar_dir = os.path.dirname(jar_path)
    jar_name = os.path.basename(jar_path)
    # 创建JAR文件的观察者
    observer = Observer()
    # 绑定事件处理器
    handler = ModifiedHandler(executor, jar_name)
    # 返回观察者
    return observer.schedule(handler, jar_dir)


def execute(args: str, sourcecode_path: str, output_files_path: str) -> (StatusCode, str, str):
    # 创建工作目录
    __TEMP_WORKDIR.mkdir(exist_ok=True)
    # 拷贝源代码文件
    shutil.copy(sourcecode_path, __TEMP_SOURCECODE)
    # 创建进程
    command = ['java', '-jar', '../Compiler.jar', args]
    process = Popen(command, cwd=__TEMP_WORKDIR, stdout=PIPE, stderr=PIPE)
    # 执行进程
    try:
        (stdout, stderr) = process.communicate(timeout=10)
        stdout = stdout.decode().strip()
        stderr = stderr.decode().strip()
        # 转移工作目录
        shutil.copy(__TEMP_WORKDIR, output_files_path)
        shutil.rmtree(__TEMP_WORKDIR)
        # 判断是否有RE
        if stderr != "":
            return StatusCode.EXECUTE_RE, stdout, stderr
        else:
            return StatusCode.EXECUTE_OK, stdout, ""
    except TimeoutExpired:
        process.kill()
        # 转移工作目录
        shutil.copy(__TEMP_WORKDIR, output_files_path)
        shutil.rmtree(__TEMP_WORKDIR)
        return StatusCode.EXECUTE_TLE, "", ""
