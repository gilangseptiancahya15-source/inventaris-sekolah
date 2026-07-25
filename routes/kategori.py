from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import login_required
from models import Kategori
from extensions import db
from sqlalchemy import exc

kategori_bp = Blueprint('kategori', __name__, url_prefix='/kategori')

@kategori_bp.route('/')
@login_required
def index():
    # Fitur Pencarian (Search)
    search = request.args.get('search', '').strip()
    if search:
        # Menggunakan ilike() khusus PostgreSQL untuk pencarian case-insensitive
        kategoris = Kategori.query.filter(Kategori.nama_kategori.ilike(f'%{search}%')).order_by(Kategori.created_at.desc()).all()
    else:
        kategoris = Kategori.query.order_by(Kategori.created_at.desc()).all()
    
    return render_template('kategori/index.html', kategoris=kategoris, search=search)

@kategori_bp.route('/add', methods=['POST'])
@login_required
def add():
    nama_kategori = request.form.get('nama_kategori', '').strip()
    deskripsi = request.form.get('deskripsi', '').strip()

    # Server Validation (Data kosong / Min Length)
    if not nama_kategori or len(nama_kategori) < 3:
        flash("Nama kategori wajib diisi dan minimal 3 karakter.", "danger")
        return redirect(url_for('kategori.index'))

    # Mengecek duplikasi nama kategori (Case-Insensitive)
    existing = Kategori.query.filter(Kategori.nama_kategori.ilike(nama_kategori)).first()
    if existing:
        flash(f"Kategori '{nama_kategori}' sudah ada di database.", "warning")
        return redirect(url_for('kategori.index'))

    # Menambahkan data baru
    new_kategori = Kategori(nama_kategori=nama_kategori, deskripsi=deskripsi)
    try:
        db.session.add(new_kategori)
        db.session.commit()
        flash("Kategori baru berhasil ditambahkan.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan sistem saat menyimpan data.", "danger")
        
    return redirect(url_for('kategori.index'))

@kategori_bp.route('/edit/<uuid:id>', methods=['POST'])
@login_required
def edit(id):
    kategori = Kategori.query.get_or_404(id)
    nama_kategori = request.form.get('nama_kategori', '').strip()
    deskripsi = request.form.get('deskripsi', '').strip()

    # Server Validation
    if not nama_kategori or len(nama_kategori) < 3:
        flash("Nama kategori wajib diisi dan minimal 3 karakter.", "danger")
        return redirect(url_for('kategori.index'))

    # Cek duplikasi menggunakan ILIKE dan validasi ID di Python agar aman dari UUID DataError
    existing = Kategori.query.filter(Kategori.nama_kategori.ilike(nama_kategori)).first()
    if existing and existing.id != id:
        flash(f"Kategori dengan nama '{nama_kategori}' sudah digunakan.", "warning")
        return redirect(url_for('kategori.index'))

    kategori.nama_kategori = nama_kategori
    kategori.deskripsi = deskripsi
    
    try:
        db.session.commit()
        flash("Data kategori berhasil diperbarui.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan sistem saat memperbarui data.", "danger")

    return redirect(url_for('kategori.index'))

@kategori_bp.route('/delete/<uuid:id>', methods=['POST'])
@login_required
def delete(id):
    kategori = Kategori.query.get_or_404(id)
    try:
        db.session.delete(kategori)
        db.session.commit()
        flash("Kategori berhasil dihapus.", "success")
    except exc.IntegrityError:
        # Constraint Supabase (RESTRICT) mencegah penghapusan jika ada relasi
        db.session.rollback()
        flash("Kategori tidak dapat dihapus karena saat ini masih digunakan oleh data barang inventaris. Hapus barang yang bersangkutan terlebih dahulu.", "danger")
    except Exception as e:
        db.session.rollback()
        flash("Terjadi kesalahan sistem saat menghapus data.", "danger")
        
    return redirect(url_for('kategori.index'))
