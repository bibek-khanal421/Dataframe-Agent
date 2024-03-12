from .generatecode import GenerateCode
from .executecode import ExecuteCode
from .validateresult import ValidateResult
from typing import Dict, List
from config.configtracker import ConfigTracker

class PipelineGenerator:
    def __init__(self, config: ConfigTracker=None, dfs: List = None, query: str = None):
        self.config = config 
        self.dfs = dfs 
        self.query = query

    def _generate_pipeline(self):
        pipeline = [
            GenerateCode,
            ExecuteCode,
            ValidateResult
        ]
        return pipeline 
    
    def run(self):
        pipeline = self._generate_pipeline()
        for module in pipeline:
            data = module(self.config, self.dfs, self.query).execute()
            self.config = data.get("config")
            self.dfs = data.get("dfs")
            self.query = data.get("query")
        result = self.config.get("validated_result")
        return result 
    
