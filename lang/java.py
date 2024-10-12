import os
import shutil
from pathlib import Path
from subprocess import Popen, PIPE, TimeoutExpired
from typing import Tuple, Callable

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from lang.common import Lang
from util.statuscode import StatusCode


class Java(Lang):
    __TEMP_BASE = Path("./runtime/java/")
    __TEMP_JAR_PATH = __TEMP_BASE / "Compiler.jar"
    __TEMP_WORKDIR = __TEMP_BASE / "workdir"
    __TEMP_SOURCECODE_PATH = __TEMP_WORKDIR / "testfile.txt"

    class ModifiedHandler(FileSystemEventHandler):
        def __init__(self, executor_start: Callable, jar_name: str, temp_jar_path: Path,
                     detected_hook: Callable[[str], None]):
            self.executor_start = executor_start
            self.jar_name = jar_name
            self.temp_jar_path = temp_jar_path
            self.detected_hook = detected_hook

        def on_created(self, event):
            if not event.is_directory and os.path.basename(event.src_path) == self.jar_name:
                shutil.copy(event.src_path, self.temp_jar_path)
                if self.detected_hook is not None:
                    self.detected_hook(self.jar_name)
                self.executor_start()

    def __init__(self, jar_path: str, detected_hook: Callable[[str], None]):
        super().__init__("Java")
        # 创建Java开发语言的文件夹
        self.__TEMP_BASE.mkdir(exist_ok=True)
        # 分析JAR文件所在文件的目录和JAR文件名
        self.jar_dir = os.path.dirname(jar_path)
        self.jar_name = os.path.basename(jar_path)
        self.detected_hook = detected_hook
        # 判断文件是否存在
        if not Path(jar_path).is_file():
            raise FileNotFoundError("The jar_path configuration was wrong.")
        shutil.copy(jar_path, self.__TEMP_JAR_PATH)

    def get_observer(self, executor_start: Callable):
        # 创建JAR文件的观察者
        observer = Observer()
        # 绑定事件处理器
        handler = self.ModifiedHandler(executor_start, self.jar_name, self.__TEMP_JAR_PATH, self.detected_hook)
        # 返回观察者
        observer.schedule(handler, self.jar_dir)
        return observer

    def execute(self, args: str, sourcecode_path: Path, compiler_output_dir: Path) -> Tuple[StatusCode, str, str]:
        # 创建工作目录
        self.__TEMP_WORKDIR.mkdir(exist_ok=True)
        # 拷贝源代码文件
        shutil.copy(sourcecode_path, self.__TEMP_SOURCECODE_PATH)
        # 创建进程
        command = ["java", "-Dfile.encoding=UTF-8", "-jar", "../Compiler.jar", args]
        process = Popen(command, cwd=self.__TEMP_WORKDIR, stdout=PIPE, stderr=PIPE, encoding="utf-8", errors="replace")
        # 执行进程
        try:
            (stdout, stderr) = process.communicate(timeout=10)
            stdout = stdout.strip()
            stderr = stderr.strip()
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
