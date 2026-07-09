import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "OCR Platform"
    app_version: str = "0.1.0"
    upload_dir: Path = Path("data/uploads")
    output_dir: Path = Path("data/outputs")
    default_ocr_engine: str = "mock"
    production: bool = os.getenv("PRODUCTION", "false").lower() == "true"
    azure_project_endpoint: str = os.getenv("AZURE_PROJECT_ENDPOINT", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    llm_model: str = os.getenv("LLM_MODEL", "")
    slm_model: str = os.getenv("SLM_MODEL", "")
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    settings = Settings()
    settings.upload_dir.mkdir(parents=True, exist_ok=True)
    settings.output_dir.mkdir(parents=True, exist_ok=True)
    return settings
