import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-only-for-dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("DATABASE_URL belum diatur. Pastikan Environment Variables sudah terisi.")
  
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Konfigurasi Upload File Gambar (maksimal 5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB
