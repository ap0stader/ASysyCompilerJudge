from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple

from util.statuscode import StatusCode


class Judge(ABC):
    __name: str

    def __init__(self, name: str):
        self.__name = name

    def name(self) -> str:
        return self.__name

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def judge(self, compiler_output_path: Path, input_path: Path, answer_path: Path) -> Tuple[StatusCode, dict]:
        pass
