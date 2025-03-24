import os


class Config:
    @staticmethod
    def get_api_url() -> str:
        return os.getenv("API_URL")

    @staticmethod
    def get_api_key() -> str:
        return os.getenv("API_KEY")
