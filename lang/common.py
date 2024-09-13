from abc import ABC, abstractmethod
from typing import Tuple

from util.statuscode import StatusCode


class Lang(ABC):
    @abstractmethod
    def get_observer(self, executor: Exception, **kwargs):
        pass

    @abstractmethod
    def execute(self, args: str, sourcecode_path: str, compiler_all_output_path: str) -> Tuple[StatusCode, str, str]:
        pass
