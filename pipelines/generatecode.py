from .base import BaseLogicUnit
from pandas import DataFrame
from typing import List
from langchain_openai import ChatOpenAI
from decouple import config 
from config.configtracker import ConfigTracker
from llm.openai import OpenAI
from llm.base import LLM
from typing import List
import io

class GenerateCode(BaseLogicUnit):

    def __init__(self, configtracker: ConfigTracker = None, dfs: List = None, query: str = None):
        super(GenerateCode, self).__init__(config=configtracker)
        self.dfs = dfs
        self.query = query
        self.llm = LLM(OpenAI(temperature=0.3))

    def _get_dataframe_info(self, df:DataFrame):
        buf = io.StringIO()
        df.info(buf=buf, verbose=False)
        info = buf.getvalue()
        return str(info)
        
    def execute(self):
        prompt = f"""
        Dataframe Information: 
        {[ f"dfs[{i}]:/n/n" + self._get_dataframe_info(df) + "/n/n" for i, df in enumerate(self.dfs)]}
        Generate me a executable python code for pandas using the above dataframe description and user question
        The code should generate a result to satisfy the user question.

        NOTE: the input to the code is a  `List(pd.DataFrame)` object named `dfs` which is already supplied to the code

        Q: {self.query}

        if the user asks for any type of plot then only generate the dataframe required for the plot and not the plot itself

        generate the result as a dictionary containing two variables type and table 
        the type specifies the type of plot eg: line, scatter, bar, pie, table etc.
        the table contains the dataframe required for the plot
        
        save the result in a variable named `result`
        """ + """
        example: ```result = {"type": "table", "table": dataframe}``` or ```result = {"type": "line", "table": dataframe}``` or ```result = {"type": "scatter", "table": dataframe}```
        
        Write code without any ``` formatting

        code:
        """
        self.config.set("pandas_code_generation_prompt", prompt)
        response = self.llm.completion(prompt)
        self.config.set("pandas_code_generation_response", response)
        return {
            "config": self.config, 
            "dfs": self.dfs,
            "query": self.query
        }

