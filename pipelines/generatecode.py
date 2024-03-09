from .base import BaseLogicUnit
from pandas import DataFrame
from typing import List
from langchain_openai import ChatOpenAI
from decouple import config 
from config.configtracker import ConfigTracker

class GenerateCode(BaseLogicUnit):

    def __init__(self, configtracker: ConfigTracker = None, dfs: DataFrame = None, query: str = None):
        super(GenerateCode, self).__init__(config=configtracker)
        self.dfs = dfs
        self.query = query
        self.llm = ChatOpenAI(temperature=0.3, openai_api_key=config("OPENAI_API_KEY"), model="gpt-4")

    def completion(self, prompt: str):
        result = self.llm.invoke(prompt)
        return result.content
        
    def execute(self):
        prompt = f"""
        Dataframe Information: {str(self.dfs)}
        Generate me a executable python code for pandas using the above dataframe description and user question
        The code should generate a result to satisfy the user question.

        NOTE: the input to the code is a `pd.DataFrame` object named `dfs`

        Q: {self.query}

        return the result in a variable named `result`
        code:
        """
        self.config.set("pandas_code_generation_prompt", prompt)
        response = self.completion(prompt)
        self.config.set("pandas_code_generation_response", response)
        return {"result": self.completion(prompt), 
                "config": self.config }

