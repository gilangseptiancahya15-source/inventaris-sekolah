"""
utils/kode_barang.py

Fungsi helper untuk pembuatan Kode Barang otomatis berdasarkan kategori.

Format Kode: [PREFIX_KATEGORI]-[NOMOR_URUT_3_DIGIT]
Contoh: MJA-001, MJA-002, KRS-001, KMP-001
"""

import re
from models import BarangInventaris, Kategori


def _buat_prefix(nama_kategori: str) -> str:
    """
    Menghasilkan prefix 3 huruf dari nama kategori.
    Algoritma: ambil huruf awal dari setiap kata (maks 3), lalu uppercase.
    Jika kata hanya satu, ambil huruf ke-1, ke-2, ke-4 (atau posisi yang ada).
    
    Contoh:
        'MEJA'         -> 'MJA'  (konsonan pertama yang ada)
        'KURSI'        -> 'KRS'
        'KOMPUTER'     -> 'KMP'
        'ALAT TULIS'   -> 'ALT'
        'ELEKTRONIK'   -> 'ELK'
    """
    nama = nama_kategori.upper().strip()
    kata_list = nama.split()

    if len(kata_list) >= 3:
        # Ambil huruf pertama dari 3 kata pertama
        return ''.join(k[0] for k in kata_list[:3])
    elif len(kata_list) == 2:
        # Dua kata: 1 huruf dari kata pertama + 2 huruf dari kata kedua
        return kata_list[0][0] + kata_list[1][:2]
    else:
        # Satu kata: ambil konsonan pertama yang ada (huruf 0, 1, 3 atau sesuai panjang)
        kata = re.sub(r'[^A-Z]', '', nama)  # Hanya huruf
        if len(kata) >= 3:
            return kata[0] + kata[1] + kata[3] if len(kata) > 3 else kata[:3]
        return kata.ljust(3, 'X')[:3]


def generate_kode_barang(kategori_id: str) -> str:
    """
    Menghasilkan kode barang unik berdasarkan ID kategori.
    
    Logika:
    1. Dapatkan nama kategori dari DB.
    2. Buat prefix 3 huruf dari nama kategori.
    3. Cari kode barang terakhir dengan prefix yang sama.
    4. Tambahkan 1 ke nomor urut terakhir.
    5. Format: PREFIX-001, PREFIX-002, dst.
    
    Args:
        kategori_id: UUID dari kategori yang dipilih.
    
    Returns:
        Kode barang unik dalam format 'XXX-NNN'.
    """
    kategori = Kategori.query.get(kategori_id)
    if not kategori:
        return f"BRG-{str(kategori_id)[:3].upper()}"

    prefix = _buat_prefix(kategori.nama_kategori)
    
    # Cari kode barang yang punya prefix sama untuk hitung urutan
    existing = BarangInventaris.query.filter(
        BarangInventaris.kode_barang.like(f'{prefix}-%')
    ).order_by(BarangInventaris.kode_barang.desc()).all()
    
    # Ekstrak nomor terakhir yang valid dari prefix ini
    max_nomor = 0
    for b in existing:
        parts = b.kode_barang.split('-')
        if len(parts) == 2 and parts[0] == prefix:
            try:
                nomor = int(parts[1])
                if nomor > max_nomor:
                    max_nomor = nomor
            except ValueError:
                pass
    
    nomor_baru = max_nomor + 1
    kode = f"{prefix}-{nomor_baru:03d}"
    
    # Pastikan kode belum digunakan (collision safety)
    while BarangInventaris.query.filter_by(kode_barang=kode).first():
        nomor_baru += 1
        kode = f"{prefix}-{nomor_baru:03d}"
    
    return kode
