class Prompt:
    def __init__(self, prompt_class):
        self.prompt_class = prompt_class
    
    def get(self):
        return self.prompt_class.get_prompt()

   