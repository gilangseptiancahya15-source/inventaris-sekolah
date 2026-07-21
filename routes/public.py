from flask import Blueprint, render_template, request
from models import BarangInventaris, Kategori
from extensions import db
from sqlalchemy import func

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    # Statistik Card Data
    total_kategori = Kategori.query.count()
    total_barang = db.session.query(func.sum(BarangInventaris.jumlah)).scalar() or 0
    baik = db.session.query(func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Baik').scalar() or 0
    rusak_ringan = db.session.query(func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Ringan').scalar() or 0
    rusak_berat = db.session.query(func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Berat').scalar() or 0
    
    # Aktivitas Terbaru (5 Barang terakhir diinput)
    recent_items = BarangInventaris.query.order_by(BarangInventaris.created_at.desc()).limit(5).all()

    # Data Grafik Kategori
    kategori_data = db.session.query(
        Kategori.nama_kategori,
        func.sum(BarangInventaris.jumlah)
    ).join(BarangInventaris, Kategori.id == BarangInventaris.kategori_id).group_by(Kategori.nama_kategori).all()
    
    label_kategori = [k[0] for k in kategori_data]
    data_kategori = [k[1] for k in kategori_data]

    # Data Grafik Kondisi
    label_kondisi = ['Baik', 'Rusak Ringan', 'Rusak Berat']
    data_kondisi = [baik, rusak_ringan, rusak_berat]

    return render_template('publik/home.html',
                           total_kategori=total_kategori,
                           total_barang=total_barang,
                           baik=baik,
                           rusak_ringan=rusak_ringan,
                           rusak_berat=rusak_berat,
                           recent_items=recent_items,
                           label_kategori=label_kategori,
                           data_kategori=data_kategori,
                           label_kondisi=label_kondisi,
                           data_kondisi=data_kondisi)

@public_bp.route('/inventaris')
def inventaris():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    kategori_filter = request.args.get('kategori', '')
    kondisi_filter = request.args.get('kondisi', '')

    query = BarangInventaris.query
    
    if search:
        query = query.filter((BarangInventaris.nama_barang.ilike(f'%{search}%')) | 
                             (BarangInventaris.kode_barang.ilike(f'%{search}%')))
    
    if kategori_filter:
        query = query.filter_by(kategori_id=kategori_filter)
        
    if kondisi_filter:
        query = query.filter_by(kondisi=kondisi_filter)
        
    # Urutkan berdasarkan yang terbaru
    query = query.order_by(BarangInventaris.created_at.desc())
    
    # Pagination (10 per halaman)
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    
    # Untuk dropdown filter
    kategori_list = Kategori.query.order_by(Kategori.nama_kategori.asc()).all()

    return render_template('publik/inventaris.html', 
                           pagination=pagination, 
                           kategori_list=kategori_list,
                           search=search,
                           kategori_filter=kategori_filter,
                           kondisi_filter=kondisi_filter)

@public_bp.route('/inventaris/<id>')
def detail(id):
    barang = BarangInventaris.query.get_or_404(id)
    return render_template('publik/detail.html', barang=barang)

@public_bp.route('/statistik')
def statistik():
    # Sama seperti home, tetapi bisa kita kembangkan lebih detail
    baik = db.session.query(func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Baik').scalar() or 0
    rusak_ringan = db.session.query(func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Ringan').scalar() or 0
    rusak_berat = db.session.query(func.sum(BarangInventaris.jumlah)).filter_by(kondisi='Rusak Berat').scalar() or 0

    kategori_data = db.session.query(
        Kategori.nama_kategori,
        func.sum(BarangInventaris.jumlah)
    ).outerjoin(BarangInventaris, Kategori.id == BarangInventaris.kategori_id).group_by(Kategori.nama_kategori).all()
    
    label_kategori = [k[0] for k in kategori_data]
    # Ganti None dengan 0 jika kategori belum ada barangnya
    data_kategori = [k[1] or 0 for k in kategori_data]

    label_kondisi = ['Baik', 'Rusak Ringan', 'Rusak Berat']
    data_kondisi = [baik, rusak_ringan, rusak_berat]

    return render_template('publik/statistik.html',
                           label_kategori=label_kategori,
                           data_kategori=data_kategori,
                           label_kondisi=label_kondisi,
                           data_kondisi=data_kondisi)
