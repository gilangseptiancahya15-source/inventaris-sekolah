from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from models import BarangInventaris, Kategori
from app import db
from datetime import datetime
from sqlalchemy import exc

barang_bp = Blueprint('barang', __name__, url_prefix='/barang')

@barang_bp.route('/')
@login_required
def index():
    # Menangkap parameter Filter dan Search
    search = request.args.get('search', '').strip()
    kategori_id = request.args.get('kategori', '')
    kondisi = request.args.get('kondisi', '')

    # Membangun Query Dasar
    query = BarangInventaris.query

    # Mengaplikasikan filter secara dinamis
    if search:
        query = query.filter(BarangInventaris.nama_barang.ilike(f'%{search}%') | BarangInventaris.kode_barang.ilike(f'%{search}%'))
    if kategori_id:
        query = query.filter_by(kategori_id=kategori_id)
    if kondisi:
        query = query.filter_by(kondisi=kondisi)

    # Mengeksekusi Query
    barangs = query.order_by(BarangInventaris.created_at.desc()).all()
    kategoris = Kategori.query.order_by(Kategori.nama_kategori).all()

    return render_template('barang/index.html', 
                           barangs=barangs, 
                           kategoris=kategoris,
                           search=search,
                           selected_kategori=kategori_id,
                           selected_kondisi=kondisi)

@barang_bp.route('/add', methods=['POST'])
@login_required
def add():
    kode_barang = request.form.get('kode_barang', '').strip()
    nama_barang = request.form.get('nama_barang', '').strip()
    kategori_id = request.form.get('kategori_id')
    jumlah = request.form.get('jumlah', type=int)
    kondisi = request.form.get('kondisi')
    lokasi = request.form.get('lokasi', '').strip()
    tanggal_masuk = request.form.get('tanggal_masuk')
    deskripsi = request.form.get('deskripsi', '').strip()

    # Server Validation: Data Kosong
    if not kode_barang or not nama_barang or not kondisi or not tanggal_masuk:
        flash("Silakan lengkapi semua field yang diwajibkan (bertanda bintang).", "danger")
        return redirect(url_for('barang.index'))
        
    # Server Validation: Kategori Harus Ada
    if not kategori_id or not Kategori.query.get(kategori_id):
        flash("Kategori barang wajib dipilih dari opsi yang tersedia.", "danger")
        return redirect(url_for('barang.index'))
        
    # Server Validation: Jumlah Minimal 1
    if jumlah is None or jumlah < 1:
        flash("Jumlah stok barang minimal harus 1 unit.", "danger")
        return redirect(url_for('barang.index'))

    # Server Validation: Kode Barang Unik
    if BarangInventaris.query.filter_by(kode_barang=kode_barang).first():
        flash(f"Kode Barang '{kode_barang}' sudah terdaftar. Gunakan kode lain.", "warning")
        return redirect(url_for('barang.index'))

    # String Date to Python Date object
    try:
        tgl_masuk = datetime.strptime(tanggal_masuk, '%Y-%m-%d').date() if tanggal_masuk else None
    except ValueError:
        tgl_masuk = None

    # Mengambil ID Admin dari session
    admin_id = session.get('admin_id')

    new_barang = BarangInventaris(
        kode_barang=kode_barang,
        nama_barang=nama_barang,
        kategori_id=kategori_id,
        jumlah=jumlah,
        kondisi=kondisi,
        lokasi=lokasi,
        tanggal_masuk=tgl_masuk,
        deskripsi=deskripsi,
        ditambahkan_oleh=admin_id
    )

    try:
        db.session.add(new_barang)
        db.session.commit()
        flash("Barang baru berhasil ditambahkan.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan saat menyimpan data.", "danger")

    return redirect(url_for('barang.index'))

@barang_bp.route('/edit/<uuid:id>', methods=['POST'])
@login_required
def edit(id):
    barang = BarangInventaris.query.get_or_404(id)
    
    kode_barang = request.form.get('kode_barang', '').strip()
    
    nama_barang = request.form.get('nama_barang', '').strip()
    kategori_id = request.form.get('kategori_id')
    jumlah = request.form.get('jumlah', type=int)
    kondisi = request.form.get('kondisi')
    lokasi = request.form.get('lokasi', '').strip()
    deskripsi = request.form.get('deskripsi', '').strip()
    tanggal_masuk = request.form.get('tanggal_masuk')

    # Server Validation: Data Kosong
    if not kode_barang or not nama_barang or not kondisi or not tanggal_masuk:
        flash("Form tidak lengkap. Pastikan semua field wajib telah diisi.", "danger")
        return redirect(url_for('barang.index'))
        
    # Server Validation: Kategori Harus Ada
    if not kategori_id or not Kategori.query.get(kategori_id):
        flash("Kategori barang tidak valid.", "danger")
        return redirect(url_for('barang.index'))
        
    # Server Validation: Jumlah Minimal 1
    if jumlah is None or jumlah < 1:
        flash("Jumlah stok barang minimal harus 1 unit.", "danger")
        return redirect(url_for('barang.index'))
    
    # Server Validation: Kode Barang Unik (kecuali entitasnya sendiri)
    if BarangInventaris.query.filter(BarangInventaris.kode_barang == kode_barang, BarangInventaris.id != id).first():
        flash(f"Kode Barang '{kode_barang}' sudah digunakan oleh barang lain.", "warning")
        return redirect(url_for('barang.index'))
        
    barang.kode_barang = kode_barang
    barang.nama_barang = nama_barang
    barang.kategori_id = kategori_id
    barang.jumlah = jumlah
    barang.kondisi = kondisi
    barang.lokasi = lokasi
    barang.deskripsi = deskripsi
    
    if tanggal_masuk:
        try:
            barang.tanggal_masuk = datetime.strptime(tanggal_masuk, '%Y-%m-%d').date()
        except ValueError:
            pass

    try:
        db.session.commit()
        flash("Data barang berhasil diperbarui.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan saat memperbarui data.", "danger")

    return redirect(url_for('barang.index'))

@barang_bp.route('/delete/<uuid:id>', methods=['POST'])
@login_required
def delete(id):
    barang = BarangInventaris.query.get_or_404(id)
    try:
        db.session.delete(barang)
        db.session.commit()
        flash("Barang berhasil dihapus dari sistem.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan saat menghapus barang.", "danger")

    return redirect(url_for('barang.index'))
