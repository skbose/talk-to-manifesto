from abc import ABC, abstractmethod


class BaseSTT(ABC):
    @abstractmethod
    def extract_text(self, audio_file: str) -> str:
        pass
