from pydantic import BaseSettings, AnyUrl
from datetime import timedelta

class Settings(BaseSettings):
    APP_NAME: str = "CRM API Gateway"
    ENV: str = "dev"

    JWT_SECRET: str = "CHANGE_ME"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60

    #TODO change to postgres
    DATABASE_URL: str = "sqlite+aiosqlite:///./users.db"

    CUSTOMER_SERVICE_ADDR: str = "localhost:50051"
    ORDER_SERVICE_ADDR: str = "localhost:50052"

    CORS_ORIGINS: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8000"]

    class Config:
        env_file = ".env"

settings = Settings()

def jwt_exp_delta():
    return timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
