import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Port aplikasi, default 5000
    APP_PORT = int(os.getenv("APP_PORT", 5000))
    
    # Base URL aplikasi
    BASE_URL = os.getenv("BASE_URL", f"http://localhost:{APP_PORT}")
    
    # LLM Configuration
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_TOKEN = os.getenv("LLM_TOKEN")
    
    # Database Configuration (Supabase / Postgres)
    # SQLAlchemy butuh 'postgresql://' bukan 'postgres://'
    db_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI") or "sqlite:///db/data.db"
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
