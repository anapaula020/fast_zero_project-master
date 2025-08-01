from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./sql_app.db"

    class Config:
        env_file = ".env"
