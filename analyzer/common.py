from abc import ABC, abstractmethod

from util.statuscode import StatusCode


class Analyzer(ABC):
    __name: str

    def __init__(self, name: str):
        self.__name = name

    def name(self) -> str:
        return self.__name

    @abstractmethod
    def register_origin(self, origin: str):
        pass

    @abstractmethod
    def prepare(self):
        pass

    @abstractmethod
    def analyze(self, status: StatusCode, origin: str, info_dict: dict):
        pass

    @abstractmethod
    def summary(self) -> str:
        pass
