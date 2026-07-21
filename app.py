from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Inisialisasi object SQLAlchemy dan Migrate (Belum terikat dengan aplikasi Flask)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Menghubungkan db dengan aplikasi Flask (Menggunakan pola Factory)
    db.init_app(app)
    
    # Mendaftarkan (import) seluruh model agar terdeteksi oleh SQLAlchemy dan Flask-Migrate
    from models import Admin, Kategori, BarangInventaris
    
    # Menghubungkan Flask-Migrate dengan aplikasi dan database
    migrate.init_app(app, db)

    @app.route('/')
    def index():
        return "<h3>Aplikasi Berjalan dan Konfigurasi Siap!</h3><p>Jika Anda melihat ini tanpa error, berarti koneksi ke Supabase sedang disiapkan secara benar.</p>"
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
