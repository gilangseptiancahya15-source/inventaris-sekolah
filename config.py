import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Secret Key — wajib diisi di Vercel Environment Variables
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-dev-key-ganti-di-produksi')

    # Database URL — ambil dari environment, konversi format jika perlu
    _db_url = os.getenv('DATABASE_URL', '')

    # Konversi format lama postgres:// ke postgresql:// (kompatibel SQLAlchemy 1.4+)
    if _db_url and _db_url.startswith("postgres://"):
        _db_url = _db_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = _db_url

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ─── Pool settings khusus untuk Serverless (Vercel) ────────────────────────
    # Di lingkungan serverless, setiap request adalah proses baru.
    # NullPool: tidak menyimpan koneksi di pool — koneksi dibuka dan langsung ditutup.
    # Ini WAJIB untuk Vercel agar tidak ada connection leak antar Lambda invocation.
    SQLALCHEMY_ENGINE_OPTIONS = {
        "poolclass": __import__("sqlalchemy.pool", fromlist=["NullPool"]).NullPool,
        "connect_args": {
            "sslmode": "require",           # SSL wajib untuk Supabase
            "connect_timeout": 10,          # Timeout 10 detik agar tidak hang
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5,
        }
    }
    # ────────────────────────────────────────────────────────────────────────────

    # Konfigurasi Upload File Gambar (maksimal 5MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB

    # Session — bertahan 1 jam, cookie aman di HTTPS (Vercel)
    PERMANENT_SESSION_LIFETIME = 3600  # detik
    SESSION_COOKIE_SECURE = os.getenv('FLASK_ENV', 'production') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
