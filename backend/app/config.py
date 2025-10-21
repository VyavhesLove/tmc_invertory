import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./inventory.db")
    SECRET_KEY = os.getenv("JWT_SECRET", "dev-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    PEPPER = os.getenv("PEPPER", "")

config = Config()
