from abc import ABC, abstractmethod

class BaseAgent(ABC):

    @abstractmethod
    def act(self, *args, **kwargs):
        NotImplementedError("act method not implemented")
        