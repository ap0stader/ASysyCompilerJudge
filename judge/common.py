from abc import ABC, abstractmethod
from pathlib import Path

from util.statuscode import StatusCode


class Judge(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def judge(self, compiler_output_path: Path, input_path: Path, answer_path: Path) -> (StatusCode, dict):
        pass
