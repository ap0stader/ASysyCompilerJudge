from abc import abstractmethod
from pathlib import Path
from typing import Tuple

from executor import ExecutorObserver
from util.statuscode import StatusCode


class Lang(ExecutorObserver):
    __name: str

    def __init__(self, name: str):
        self.__name = name

    def name(self):
        return self.__name

    @abstractmethod
    def execute(self, args: str, sourcecode_path: Path, compiler_output_dir: Path) -> Tuple[StatusCode, str, str]:
        pass
