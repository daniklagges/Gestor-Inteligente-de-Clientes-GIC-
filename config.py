import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuración global del proyecto GIC."""

    DB_PATH = os.getenv("DB_PATH", "src/database/gic.db")
    IDENTITY_API_URL = os.getenv("IDENTITY_API_URL", "")
    IDENTITY_API_KEY = os.getenv("IDENTITY_API_KEY", "")
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-key-cambiar")
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
