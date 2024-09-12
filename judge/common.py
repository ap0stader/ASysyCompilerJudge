from abc import ABC, abstractmethod


class Judge(ABC):
    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def judge(self, compiler_output_path: str, input_path: str, answer_path: str):
        pass
