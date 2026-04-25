import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_PORT = os.getenv("APP_PORT", 5000)
    BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_TOKEN = os.getenv("LLM_TOKEN")

    DB_HOST     = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT     = os.getenv("DB_PORT", "5432")
    DB_NAME     = os.getenv("DB_NAME", "")
    DB_USER     = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', 'postgres')}"
        f"@{os.getenv('DB_HOST', '127.0.0.1')}:{os.getenv('DB_PORT', '5432')}"
        f"/{os.getenv('DB_NAME', '')}"
        if os.getenv("DB_NAME")
        else os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///db/data.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False