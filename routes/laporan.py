from flask import Blueprint, render_template
from utils.decorators import login_required
from models import BarangInventaris, Kategori
from extensions import db
from sqlalchemy import func
from datetime import datetime

laporan_bp = Blueprint('laporan', __name__, url_prefix='/laporan')

@laporan_bp.route('/')
@login_required
def index():
    # 1. Total Inventaris Keseluruhan
    total_inventaris = db.session.query(func.sum(BarangInventaris.jumlah)).scalar() or 0
    total_jenis = BarangInventaris.query.count()

    # 2. Rekapitulasi Berdasarkan Kategori
    rekap_kategori = db.session.query(
        Kategori.nama_kategori,
        func.sum(BarangInventaris.jumlah).label('total')
    ).join(BarangInventaris, isouter=True).group_by(Kategori.nama_kategori).all()

    # 3. Rekapitulasi Berdasarkan Kondisi
    rekap_kondisi = db.session.query(
        BarangInventaris.kondisi,
        func.sum(BarangInventaris.jumlah).label('total')
    ).group_by(BarangInventaris.kondisi).all()

    # 4. Rekap Data Seluruh Barang untuk Tabel Rincian
    semua_barang = BarangInventaris.query.order_by(BarangInventaris.kategori_id, BarangInventaris.nama_barang).all()

    return render_template('laporan/index.html',
                           total_inventaris=total_inventaris,
                           total_jenis=total_jenis,
                           rekap_kategori=rekap_kategori,
                           rekap_kondisi=rekap_kondisi,
                           semua_barang=semua_barang,
                           current_time=datetime.now())
