"""

"""

from .base import BasePrompt

class CodeRetryPrompt(BasePrompt):

    _prompt_url = "prompt/assets/code_retry_prompt.tmpl"

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
        
    