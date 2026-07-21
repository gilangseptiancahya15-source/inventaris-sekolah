"""
utils/file_helper.py

Helper untuk pengelolaan file upload gambar barang.
Dirancang modular agar mudah diganti dari penyimpanan lokal ke cloud (Supabase Storage, dll).

CATATAN VERCEL:
  Vercel memiliki filesystem read-only di /var/task.
  Fungsi save_file() akan mencoba menyimpan ke /tmp (satu-satunya folder writable di Lambda).
  NAMUN file di /tmp bersifat ephemeral (hilang saat cold start).
  Untuk produksi permanen, ganti implementasi save_file() dan delete_file()
  agar memanggil Supabase Storage API.
"""

import os
import uuid
from werkzeug.utils import secure_filename

# =============================================
# Konfigurasi Upload
# =============================================
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE_MB = 5
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024  # 5MB in bytes

# Subfolder relatif dari static/ (untuk lokal)
UPLOAD_SUBFOLDER = 'uploads/barang'

# =============================================
# Deteksi Environment (Vercel vs Lokal)
# =============================================
IS_VERCEL = os.getenv('VERCEL') == '1' or os.getenv('AWS_LAMBDA_FUNCTION_NAME') is not None


def get_upload_folder():
    """
    Mengembalikan path absolut folder penyimpanan file upload.
    - Lokal  : static/uploads/barang/ (permanen)
    - Vercel : /tmp/uploads/barang/   (ephemeral, hanya untuk cold start)
    """
    if IS_VERCEL:
        # Di Vercel, /tmp adalah satu-satunya folder yang bisa ditulis
        folder = os.path.join('/tmp', UPLOAD_SUBFOLDER)
    else:
        from flask import current_app
        folder = os.path.join(current_app.static_folder, UPLOAD_SUBFOLDER)

    try:
        os.makedirs(folder, exist_ok=True)
    except OSError:
        pass  # Gagal buat folder, biarkan save_file() menangani errornya
    return folder


def is_allowed_file(filename: str) -> bool:
    """Mengecek apakah ekstensi file diizinkan."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_allowed_size(file_storage) -> bool:
    """
    Mengecek apakah ukuran file tidak melebihi batas maksimal.
    Membaca isi file sementara lalu mengembalikan pointer ke awal.
    """
    file_storage.seek(0, os.SEEK_END)
    size = file_storage.tell()
    file_storage.seek(0)  # kembalikan pointer
    return size <= MAX_FILE_SIZE_BYTES


def save_file(file_storage) -> str | None:
    """
    Menyimpan file ke folder lokal/tmp dan mengembalikan nama file unik.
    Mengembalikan None jika file tidak valid atau gagal disimpan.

    NOTE (Migrasi ke Supabase Storage):
        Ganti isi fungsi ini dengan panggilan ke Supabase Storage API:
            import supabase
            response = supabase.storage.from_('barang').upload(unique_filename, file_bytes)
            return unique_filename  # atau URL publik dari response
    """
    if not file_storage or file_storage.filename == '':
        return None

    if not is_allowed_file(file_storage.filename):
        return None

    if not is_allowed_size(file_storage):
        return None

    # Buat nama file unik menggunakan UUID agar tidak terjadi bentrok
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{ext}"

    try:
        save_path = os.path.join(get_upload_folder(), unique_filename)
        file_storage.save(save_path)
        return unique_filename
    except Exception:
        # Gagal simpan file — kembalikan None, jangan crash aplikasi
        return None


def delete_file(filename: str) -> bool:
    """
    Menghapus file dari folder lokal/tmp.
    Mengembalikan True jika berhasil, False jika file tidak ditemukan.

    NOTE (Migrasi ke Supabase Storage):
        Ganti dengan panggilan delete ke bucket:
            supabase.storage.from_('barang').remove([filename])
    """
    if not filename:
        return False
    try:
        path = os.path.join(get_upload_folder(), filename)
        if os.path.isfile(path):
            os.remove(path)
            return True
    except Exception:
        pass
    return False


def get_foto_url(filename: str) -> str | None:
    """
    Mengembalikan path relatif URL untuk ditampilkan di template.
    Untuk lokal: url_for('static', filename='uploads/barang/<filename>')
    Untuk Supabase Storage: kembalikan URL publik dari bucket.
    """
    if not filename:
        return None
    return f"uploads/barang/{filename}"
