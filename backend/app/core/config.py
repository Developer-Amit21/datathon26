from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Crime Intelligence Platform"
    database_url: str = "sqlite:///./crime.db"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = "demo-secret"
    jwt_algorithm: str = "HS256"
    api_prefix: str = "/api"

    class Config:
        env_file = ".env"


settings = Settings()
