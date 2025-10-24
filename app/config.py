"""Application configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # App settings
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Server
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db/sa-tax.db")
    
    # Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TAX_RATES_PATH: Path = BASE_DIR / os.getenv("TAX_RATES_PATH", "data/tax_rates.yml")
    TEMPLATES_DIR: Path = BASE_DIR / "app" / "templates"
    STATIC_DIR: Path = BASE_DIR / "app" / "static"
    
    # Admin
    ADMIN_ENABLED: bool = os.getenv("ADMIN_ENABLED", "True").lower() == "true"
    
    # Supabase (for logging submissions)
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    ENABLE_SUBMISSION_LOGGING: bool = os.getenv("ENABLE_SUBMISSION_LOGGING", "False").lower() == "true"
    
    # Google AdSense
    GOOGLE_ADSENSE_CLIENT_ID: str = os.getenv("GOOGLE_ADSENSE_CLIENT_ID", "")
    ENABLE_ADS: bool = os.getenv("ENABLE_ADS", "False").lower() == "true"


settings = Settings()
