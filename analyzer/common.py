from abc import ABC, abstractmethod

from util.statuscode import StatusCode


class Analyzer(ABC):
    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def info(self, status: StatusCode, info):
        pass

    @abstractmethod
    def summary_print(self):
        pass

    @abstractmethod
    def summary_save(self) -> str:
        pass
