from abc import ABC, abstractmethod


class LLMInterface(ABC):
    """
        LLM acts like a brain
    """
    @abstractmethod
    def thinking(self, memory:list[dict], role_prompt:str, stream:bool):
        pass

    

    

