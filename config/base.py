from abc import ABC, abstractmethod

class BaseConfig(ABC):

    @abstractmethod
    def get(self, *args, **kwargs):
        raise NotImplementedError("Error Function Not Implemented!")
    
    @abstractmethod
    def set(self, *args, **kwargs):
        raise NotImplementedError("Error Function Not Implemented!")
    
    @abstractmethod
    def remove(self, *args, **kwargs):
        raise NotImplementedError("Error Function Not Implemented!")