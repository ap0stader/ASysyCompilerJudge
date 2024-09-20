import os
import shutil
import sys
from pathlib import Path
from subprocess import Popen, PIPE, TimeoutExpired
from typing import Tuple

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from executor import Executor
from lang.common import Lang
from util.statuscode import StatusCode
from util.termcolor import RESET, INVERT


class Java(Lang):
    __TEMP_BASE = Path("./runtime/java/")
    __TEMP_JAR_PATH = __TEMP_BASE / "Compiler.jar"
    __TEMP_WORKDIR = __TEMP_BASE / "workdir"
    __TEMP_SOURCECODE_PATH = __TEMP_WORKDIR / "testfile.txt"

    class ModifiedHandler(FileSystemEventHandler):
        def __init__(self, executor: Executor, jar_name: str, temp_jar_path: Path):
            self.executor = executor
            self.jar_name = jar_name
            self.temp_jar_path = temp_jar_path

        def on_created(self, event):
            if not event.is_directory and os.path.basename(event.src_path) == self.jar_name:
                print("New " + INVERT + self.jar_name + RESET + " has been detected", end="")
                shutil.copy(event.src_path, self.temp_jar_path)
                print(" and copied.")
                self.executor.start()

    def __init__(self, jar_path: str):
        # 创建Java开发语言的文件夹
        self.__TEMP_BASE.mkdir(exist_ok=True)
        # 分析JAR文件所在文件的目录和JAR文件名
        self.jar_dir = os.path.dirname(jar_path)
        self.jar_name = os.path.basename(jar_path)
        # 判断文件是否存在
        if not Path(jar_path).is_file():
            print("The JAR file configuration was wrong.", file=sys.stderr)
            exit(1)
        shutil.copy(jar_path, self.__TEMP_JAR_PATH)

    def get_observer(self, executor: Executor):
        print(">>> Creating Java Observer...")
        # 创建JAR文件的观察者
        observer = Observer()
        # 绑定事件处理器
        handler = self.ModifiedHandler(executor, self.jar_name, self.__TEMP_JAR_PATH)
        # 返回观察者
        observer.schedule(handler, self.jar_dir)
        return observer

    def execute(self, args: str, sourcecode_path: Path, compiler_output_dir: Path) -> Tuple[StatusCode, str, str]:
        # 创建工作目录
        self.__TEMP_WORKDIR.mkdir(exist_ok=True)
        # 拷贝源代码文件
        shutil.copy(sourcecode_path, self.__TEMP_SOURCECODE_PATH)
        # 创建进程
        command = ["java", "-jar", "../Compiler.jar", args]
        process = Popen(command, cwd=self.__TEMP_WORKDIR, stdout=PIPE, stderr=PIPE)
        # 执行进程
        try:
            (stdout, stderr) = process.communicate(timeout=10)
            stdout = stdout.decode().strip()
            stderr = stderr.decode().strip()
            # 转移工作目录
            shutil.copytree(self.__TEMP_WORKDIR, compiler_output_dir, dirs_exist_ok=True)
            shutil.rmtree(self.__TEMP_WORKDIR)
            # 判断是否有RE
            if stderr != "":
                return StatusCode.EXECUTE_RE, stdout, stderr
            else:
                return StatusCode.EXECUTE_OK, stdout, ""
        except TimeoutExpired:
            process.kill()
            # 转移工作目录
            shutil.copytree(self.__TEMP_WORKDIR, compiler_output_dir, dirs_exist_ok=True)
            shutil.rmtree(self.__TEMP_WORKDIR)
            return StatusCode.EXECUTE_TLE, "", ""
