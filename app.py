from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from utils.decorators import login_required
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

    # Registrasi Blueprints
    from routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    @app.route('/')
    @login_required
    def index():
        from models import Kategori, BarangInventaris
        
        # Statistik Card Data
        total_kategori = Kategori.query.count()
        # Menggunakan sum() untuk menjumlahkan kolom 'jumlah' barang fisik
        total_barang = db.session.query(db.func.sum(BarangInventaris.jumlah)).scalar() or 0
        baik = db.session.query(db.func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Baik').scalar() or 0
        rusak_ringan = db.session.query(db.func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Ringan').scalar() or 0
        rusak_berat = db.session.query(db.func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Berat').scalar() or 0
        
        # Aktivitas Terbaru (5 Barang terakhir diinput)
        recent_items = BarangInventaris.query.order_by(BarangInventaris.created_at.desc()).limit(5).all()

        return render_template('dashboard/index.html',
                               total_kategori=total_kategori,
                               total_barang=total_barang,
                               baik=baik,
                               rusak_ringan=rusak_ringan,
                               rusak_berat=rusak_berat,
                               recent_items=recent_items)
        
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
