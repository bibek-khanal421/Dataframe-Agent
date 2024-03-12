from langchain_openai import ChatOpenAI

from secret_manager.secret import SecretManager

from .base import BaseLLM


class OpenAI(BaseLLM):
    def __init__(
        self, temperature: float = None, openai_api_key: str = None, model: str = None
    ):
        self.secret_manager = SecretManager()
        self.temperature = temperature if temperature else 0.3
        self.openai_api_key = (
            openai_api_key
            if openai_api_key
            else self.secret_manager.get_from_env("OPENAI_API_KEY")
        )
        self.model = (
            model if model else self.secret_manager.get_from_env("OPENAI_MODEL")
        )

    def get_llm(self):
        llm = ChatOpenAI(
            temperature=self.temperature,
            openai_api_key=self.openai_api_key,
            model=self.model,
        )
        return llm

    def completion(self, prompt: str):
        llm = self.get_llm()
        result = llm.invoke(prompt)
        return result.content
