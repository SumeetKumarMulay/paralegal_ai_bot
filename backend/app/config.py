import os


class Config:
    @staticmethod
    def get_mcp_india_kanoon_url() -> str:
        return os.getenv("MCP_INDIA_KANOON_URL")

    @staticmethod
    def open_api_key() -> str:
        return os.getenv("OPEN_AI_KEY")

    @staticmethod
    def open_ai_url() -> str:
        return os.getenv("OPEN_AI_URL")

    @staticmethod
    def ai_model() -> str:
        return os.getenv("OPEN_AI_MODEL")
