from abc import abstractmethod
from pathlib import Path
from typing import Tuple

from executor import ExecutorObserver
from util.statuscode import StatusCode


class Lang(ExecutorObserver):
    @abstractmethod
    def execute(self, args: str, sourcecode_path: Path, compiler_output_dir: Path) -> Tuple[StatusCode, str, str]:
        pass
