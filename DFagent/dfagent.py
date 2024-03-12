from .base import BaseAgent
from pipelines.pipelineexecutor import PipelineGenerator
from config.configtracker import ConfigTracker
from typing import Dict, List

class Agent(BaseAgent):
    def __init__(self, dfs:List = None, config: Dict=None):
        self.dfs = dfs 
        self.configtracker = ConfigTracker()
        self.config = config

    def _validate_type(self):
        # checking if dfs is type list and contains dataframe
        if isinstance(self.dfs, List) and len(self.dfs) == 0:
            raise("parameter dfs should contain a list of dataframe")
        if isinstance(self.configtracker, ConfigTracker):
            raise("'config' should be an object of Dict type")

    def act(self, query: str = None):
        result = PipelineGenerator(self.configtracker, self.dfs, query).run()
        return result