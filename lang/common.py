from abc import abstractmethod
from typing import Tuple

from executor import ExecutorObserver
from util.statuscode import StatusCode


class Lang(ExecutorObserver):
    @abstractmethod
    def execute(self, args: str, sourcecode_path: str, compiler_all_output_path: str) -> Tuple[StatusCode, str, str]:
        pass
