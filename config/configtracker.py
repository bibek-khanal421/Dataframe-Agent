from .base import BaseConfig
from typing import Any

class ConfigTracker(BaseConfig):

    def __init__(self, config: dict = None):
        if config:
            self.config = config 
        else:
            self.config = dict()

        
    def set(self, key:Any , value:Any):
        try:
            self.config[key]=value
        except:
            raise Exception("Error inserting to config!!!")
        
    def get(self, key:Any):
        try:
            return self.config[key]
        except:
            raise Exception("key not found!!!")
        
    def remove(self, key:Any):
        try:
            del self.config[key]
        except:
            raise Exception("key not found!!!")

