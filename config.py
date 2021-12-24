from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "API scraper"
    api_key: str

    class Config:
        env_file = ".env"

settings = Settings()