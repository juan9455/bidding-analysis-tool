"""
Application Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Application Configuration
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
APP_NAME = os.getenv("APP_NAME", "Bidding Analysis Tool")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

# File Upload Configuration
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 52428800))  # 50MB
ALLOWED_EXTENSIONS = {
    "pdf", "doc", "docx", "xls", "xlsx", "txt",
    "png", "jpg", "jpeg", "bmp", "gif"
}

# Database Configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./bidding_analysis.db"
)

# CORS Configuration
CORS_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:3000"
).split(",")

# API Configuration
API_V1_STR = os.getenv("API_V1_STR", "/api/v1")
