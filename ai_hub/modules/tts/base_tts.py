from abc import ABC, abstractmethod


class BaseTTS(ABC):
    @abstractmethod
    def stream(self, text: str):
        pass

    @abstractmethod
    def synthesize(self, text: str):
        pass

    @abstractmethod
    def stream_and_save(self, text: str, output_dir: str) -> None:
        pass
