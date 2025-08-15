from pydantic import AnyUrl
from datetime import timedelta
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "CRM API Gateway"
    ENV: str = "dev"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRES_MINUTES: int = 60

    DATABASE_URL: str

    CUSTOMER_SERVICE_ADDR: str = "localhost:50051"
    ORDER_SERVICE_ADDR: str = "localhost:50052"

    CORS_ORIGINS: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500", "http://localhost:8000"]

    model_config = {
        "env_file": Path(__file__).resolve().parent.parent / ".env"
    }

settings = Settings()

def jwt_exp_delta():
    return timedelta(minutes=settings.JWT_EXPIRES_MINUTES)
