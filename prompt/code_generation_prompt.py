"""
Dataframe Information: 
{dataframe_info_list}
Generate me a executable python code for pandas using the above dataframe description and user question
The code should generate a result to satisfy the user question.

NOTE: the input to the code is a  `List(pd.DataFrame)` object named `dfs` which is already supplied to the code

Q: {query}

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


from .base import BasePrompt

class CodeGenerationPrompt(BasePrompt):

    _prompt_url = "prompt/assets/code_generation_prompt.tmpl"

    def __init__(self, vars):
        self.vars = vars

    def get_prompt(self):
        try:
            with open(self._prompt_url, "r") as file:
                prompt = file.read()
            prompt = self.set_var(prompt, self.vars)
            return prompt
        except Exception as e:
            raise RuntimeError(f"Error getting prompt: {e}")
        