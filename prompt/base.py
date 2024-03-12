from abc import ABC, abstractmethod

class BasePrompt(ABC):

    _prompt_url = None
    
    @abstractmethod
    def get_prompt(self, *args, **kwargs):
        pass

    def set_var(self, prompt:str, vars: dict):
        for key, value in vars.items():
            prompt = prompt.replace(f"{{{key}}}", value)
        return prompt