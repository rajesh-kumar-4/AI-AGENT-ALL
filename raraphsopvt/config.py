from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    app_name: str = "RaraphSOPVT Sample API"
    environment: str = os.getenv("ENVIRONMENT", "development")
    api_key: str = os.getenv("API_KEY", "supersecretkey")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./database.db")
    mongodb_uri: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongodb_db: str = os.getenv("MONGODB_DB", "raraphsopvt")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
