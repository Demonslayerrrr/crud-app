from pydantic_settings import BaseSettings  # ✅ instead of from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"

settings = Settings()
