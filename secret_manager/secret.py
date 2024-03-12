from decouple import config


class SecretManager:
    def __init__(self):
        pass

    def get_from_env(self, key: str):
        return config(key)
