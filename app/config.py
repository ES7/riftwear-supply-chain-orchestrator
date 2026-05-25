from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    groq_api_key: str
    groq_model: str = "llama3-8b-8192"
    excel_path: str = "data.xlsx"

    class Config:
        env_file = ".env"

settings = Settings()
EXCEL_PATH = Path(settings.excel_path)
