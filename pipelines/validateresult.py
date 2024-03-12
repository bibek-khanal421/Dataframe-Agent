from .base import BaseLogicUnit
from pandas import DataFrame
from typing import List
from config.configtracker import ConfigTracker
from llm.openai import OpenAI
from llm.base import LLM
from typing import List

class ValidateResult(BaseLogicUnit):

    def __init__(self, configtracker: ConfigTracker = None, dfs: List = None, query: str = None):
        super(ValidateResult, self).__init__(config=configtracker)
        self.dfs = dfs
        self.query = query
        self.llm = LLM(OpenAI(temperature=0.3))

    def _validate_result(self, result):
        # check if the result is a dict 
        if not isinstance(result, dict):
            return False
        # check if the result has a key 'type'
        if not "type" in result:
            return False
        # check if the result has a key 'table'
        if not "table" in result:
            return False
        
    def execute(self):
        code_execution_result = self.config.get("code_execution_result")
        if not self._validate_result(code_execution_result):
            self.config.set("validated_result", {"type": "error", "message": "Unable to find the answer to your question"})
        
        if code_execution_result.get("type") == None:
            code_execution_result['type'] = "table"
            
        self.config.set("validated_result", code_execution_result)
        return {
            "config": self.config, 
            "dfs": self.dfs,
            "query": self.query
        }
        