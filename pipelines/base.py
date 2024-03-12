from abc import ABC, abstractmethod


class BaseLogicUnit(ABC):
    def __init__(self, *args, **kwargs):
        self.config = kwargs.get("config", None)

    @abstractmethod
    def execute(self, *args, **kwargs):
        raise NotImplementedError("execute method not implemented")
