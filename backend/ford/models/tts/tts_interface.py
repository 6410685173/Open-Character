from abc import ABC, abstractmethod


class TTSInterface(ABC):
    
    @abstractmethod
    def text_to_speech(message:str):
        pass