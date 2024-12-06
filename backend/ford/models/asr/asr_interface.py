from abc import ABC, abstractmethod


class ASRInterface(ABC):

    @abstractmethod
    def speech_to_text():
        pass