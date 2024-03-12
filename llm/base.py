from abc import ABC, abstractmethod

class BaseLLM(ABC):

    @abstractmethod
    def get_llm(self):
        NotImplementedError

    @abstractmethod
    def completion(self, prompt: str):
        NotImplementedError


class LLM:
    def __init__(self, llm):
        self.llm = llm
    
    def completion(self, prompt: str):
        result = self.llm.completion(prompt)
        return result
