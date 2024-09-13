from abc import ABC, abstractmethod

from util.statuscode import StatusCode


class Analyzer(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def register_origin(self, origin: str, **kwargs):
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def analyze(self, status: StatusCode, origin: str, info_dict: dict):
        pass

    @abstractmethod
    def summary_print(self):
        pass

    @abstractmethod
    def summary_save(self) -> str:
        pass
