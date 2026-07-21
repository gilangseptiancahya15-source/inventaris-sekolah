from flask import Flask, render_template
from utils.decorators import login_required
from config import Config
from extensions import db, migrate
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Validasi DATABASE_URL setelah app dibuat (tidak saat import/build)
    if not app.config.get('SQLALCHEMY_DATABASE_URI'):
        raise RuntimeError(
            "DATABASE_URL belum diatur. "
            "Tambahkan DATABASE_URL di Vercel Environment Variables."
        )

    # Menghubungkan db dengan aplikasi Flask (Menggunakan pola Factory)
    db.init_app(app)
    
    # Mendaftarkan (import) seluruh model agar terdeteksi oleh SQLAlchemy dan Flask-Migrate
    from models import Admin, Kategori, BarangInventaris
    
    # Menghubungkan Flask-Migrate dengan aplikasi dan database
    migrate.init_app(app, db)

    # Registrasi Blueprints
    from routes.auth import auth_bp
    from routes.kategori import kategori_bp
    from routes.barang import barang_bp
    from routes.laporan import laporan_bp
    from routes.public import public_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(kategori_bp)
    app.register_blueprint(barang_bp)
    app.register_blueprint(laporan_bp)
    app.register_blueprint(public_bp)

    # ─── Error Handlers ──────────────────────────────────────────
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        db.session.rollback()  # Rollback session yang rusak agar tidak hanging
        return render_template('errors/500.html'), 500

    @app.errorhandler(413)
    def request_entity_too_large(e):
        from flask import flash, redirect, request as req
        flash("Ukuran file melebihi batas maksimal 5MB.", "warning")
        return redirect(req.referrer or '/'), 413
    # ─────────────────────────────────────────────────────────────

    @app.route('/dashboard')
    @login_required
    def dashboard():
        from models import Kategori, BarangInventaris
        
        # Statistik Card Data
        total_kategori = Kategori.query.count()
        # Konversi Decimal → int agar Chart.js berfungsi dengan benar
        total_barang = int(db.session.query(db.func.sum(BarangInventaris.jumlah)).scalar() or 0)
        baik = int(db.session.query(db.func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Baik').scalar() or 0)
        rusak_ringan = int(db.session.query(db.func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Ringan').scalar() or 0)
        rusak_berat = int(db.session.query(db.func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Berat').scalar() or 0)
        
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
    app.run(debug=False)
