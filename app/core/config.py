import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    YANDEX_CLIENT_ID: str = os.getenv("YANDEX_CLIENT_ID")
    YANDEX_CLIENT_SECRET: str = os.getenv("YANDEX_CLIENT_SECRET")
    API_SECRET_KEY: str = os.getenv("API_SECRET_KEY", "supersecret")

    class Config:
        env_file = ".env"


settings = Settings()