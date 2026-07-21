from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from utils.decorators import login_required
from utils.file_helper import save_file, delete_file, is_allowed_file, is_allowed_size, ALLOWED_EXTENSIONS, MAX_FILE_SIZE_MB
from utils.kode_barang import generate_kode_barang
from models import BarangInventaris, Kategori
from extensions import db
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


@barang_bp.route('/kode-preview', methods=['GET'])
@login_required
def kode_preview():
    """Endpoint AJAX: mengembalikan preview kode barang berdasarkan kategori yang dipilih."""
    from flask import jsonify
    kategori_id = request.args.get('kategori_id', '')
    if not kategori_id:
        return jsonify({'kode': ''})
    kode = generate_kode_barang(kategori_id)
    return jsonify({'kode': kode})


@barang_bp.route('/add', methods=['POST'])
@login_required
def add():
    nama_barang = request.form.get('nama_barang', '').strip()
    kategori_id = request.form.get('kategori_id')
    jumlah = request.form.get('jumlah', type=int)
    kondisi = request.form.get('kondisi')
    lokasi = request.form.get('lokasi', '').strip()
    tanggal_masuk = request.form.get('tanggal_masuk')
    deskripsi = request.form.get('deskripsi', '').strip()

    # Server Validation: Data Kosong
    if not nama_barang or not kondisi or not tanggal_masuk:
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

    # Generate Kode Barang Otomatis
    kode_barang = generate_kode_barang(kategori_id)

    # String Date to Python Date object
    try:
        tgl_masuk = datetime.strptime(tanggal_masuk, '%Y-%m-%d').date() if tanggal_masuk else None
    except ValueError:
        tgl_masuk = None

    # Handle Upload Gambar
    foto_filename = None
    foto_file = request.files.get('foto_barang')
    if foto_file and foto_file.filename != '':
        if not is_allowed_file(foto_file.filename):
            flash(f"Format gambar tidak valid. Format yang diizinkan: {', '.join(ALLOWED_EXTENSIONS).upper()}.", "warning")
            return redirect(url_for('barang.index'))
        if not is_allowed_size(foto_file):
            flash(f"Ukuran gambar melebihi batas maksimal {MAX_FILE_SIZE_MB}MB.", "warning")
            return redirect(url_for('barang.index'))
        foto_filename = save_file(foto_file)

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
        foto_barang=foto_filename,
        ditambahkan_oleh=admin_id
    )

    try:
        db.session.add(new_barang)
        db.session.commit()
        flash(f"Barang baru berhasil ditambahkan dengan kode <strong>{kode_barang}</strong>.", "success")
    except Exception as e:
        db.session.rollback()
        # Hapus file yang sudah terupload jika DB gagal
        if foto_filename:
            delete_file(foto_filename)
        flash("Terjadi kesalahan saat menyimpan data.", "danger")

    return redirect(url_for('barang.index'))


@barang_bp.route('/edit/<uuid:id>', methods=['POST'])
@login_required
def edit(id):
    barang = BarangInventaris.query.get_or_404(id)
    
    nama_barang = request.form.get('nama_barang', '').strip()
    kategori_id = request.form.get('kategori_id')
    jumlah = request.form.get('jumlah', type=int)
    kondisi = request.form.get('kondisi')
    lokasi = request.form.get('lokasi', '').strip()
    deskripsi = request.form.get('deskripsi', '').strip()
    tanggal_masuk = request.form.get('tanggal_masuk')
    hapus_foto = request.form.get('hapus_foto')  # Checkbox untuk hapus foto

    # Server Validation: Data Kosong
    if not nama_barang or not kondisi or not tanggal_masuk:
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
    
    # Handle Upload Gambar Baru
    foto_file = request.files.get('foto_barang')
    if foto_file and foto_file.filename != '':
        if not is_allowed_file(foto_file.filename):
            flash(f"Format gambar tidak valid. Format yang diizinkan: {', '.join(ALLOWED_EXTENSIONS).upper()}.", "warning")
            return redirect(url_for('barang.index'))
        if not is_allowed_size(foto_file):
            flash(f"Ukuran gambar melebihi batas maksimal {MAX_FILE_SIZE_MB}MB.", "warning")
            return redirect(url_for('barang.index'))
        # Hapus gambar lama sebelum simpan gambar baru
        if barang.foto_barang:
            delete_file(barang.foto_barang)
        new_foto = save_file(foto_file)
        barang.foto_barang = new_foto
    elif hapus_foto:
        # Admin secara eksplisit meminta hapus foto
        if barang.foto_barang:
            delete_file(barang.foto_barang)
        barang.foto_barang = None

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
    # Hapus file foto dari storage saat barang dihapus
    if barang.foto_barang:
        delete_file(barang.foto_barang)
    try:
        db.session.delete(barang)
        db.session.commit()
        flash("Barang berhasil dihapus dari sistem.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan saat menghapus barang.", "danger")

    return redirect(url_for('barang.index'))
