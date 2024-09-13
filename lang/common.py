from abc import ABC, abstractmethod

from watchdog.observers import Observer

from util.statuscode import StatusCode


class Lang(ABC):
    @abstractmethod
    def get_observer(self, executor: Exception, **kwargs) -> Observer:
        pass

    @abstractmethod
    def execute(self, args: str, sourcecode_path: str, compiler_all_output_path: str) -> (StatusCode, str, str):
        pass
