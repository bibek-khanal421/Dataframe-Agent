from .base import BaseLogicUnit
from pandas import DataFrame
from typing import List
from config.configtracker import ConfigTracker
from llm.openai import OpenAI
from llm.base import LLM
from typing import List
import io
from prompt.code_generation_prompt import CodeGenerationPrompt
from prompt.prompt import Prompt
from prompt.code_retry_prompt import CodeRetryPrompt

class GenerateCode(BaseLogicUnit):

    def __init__(self, configtracker: ConfigTracker = None, dfs: List = None, query: str = None):
        super(GenerateCode, self).__init__(config=configtracker)
        self.dfs = dfs
        self.query = query
        self.llm = LLM(OpenAI(temperature=0.3))

    def _get_dataframe_info(self, df:DataFrame):
        # buf = io.StringIO()
        # df.info(buf=buf, verbose=False)
        # info = buf.getvalue()
        info = df.head(1)
        return str(info)
        
    def execute(self):
        vars = {
           "dataframe_info_list" : "/n/n".join([f"dfs[{i}]:/n/n" + self._get_dataframe_info(df) for i, df in enumerate(self.dfs)]),
            "query": self.query
        }
        prompt = Prompt(CodeGenerationPrompt(vars)).get()
        self.config.set("pandas_code_generation_prompt", prompt)
        response = self.llm.completion(prompt)
        self.config.set("pandas_code_generation_response", response)
        self.config.set("retry_code_generation_function", self.retry_code_generation)
        return {
            "config": self.config, 
            "dfs": self.dfs,
            "query": self.query
        }

    def retry_code_generation(self):
        code = self.config.get("pandas_code_generation_response")
        vars = {
                "dataframe_info_list" : "/n/n".join([f"dfs[{i}]:/n/n" + self._get_dataframe_info(df) for i, df in enumerate(self.dfs)]),
                "query": self.query,
                "code": code
            }
        prompt = Prompt(CodeRetryPrompt(vars)).get()
        response = self.llm.completion(prompt)
        self.config.set("pandas_code_generation_response", response)

    