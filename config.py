import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret Key — wajib diisi di Vercel Environment Variables
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-key-ganti-di-produksi')

    # Database URL — ambil dari environment, konversi format jika perlu
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', '')

    # Konversi format lama postgres:// ke postgresql:// (kompatibel SQLAlchemy 1.4+)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Konfigurasi Upload File Gambar (maksimal 5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

    # Session — bertahan 1 jam, cookie aman di HTTPS (Vercel)
    PERMANENT_SESSION_LIFETIME = 3600  # detik
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV', 'production') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
