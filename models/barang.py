import uuid
from datetime import datetime, timezone, date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import CheckConstraint
from extensions import db

class BarangInventaris(db.Model):
    __tablename__ = 'barang_inventaris'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Foreign Keys
    kategori_id = db.Column(UUID(as_uuid=True), db.ForeignKey('kategori.id', ondelete='RESTRICT'), nullable=False)
    ditambahkan_oleh = db.Column(UUID(as_uuid=True), db.ForeignKey('admin.id', ondelete='SET NULL'), nullable=True)
    
    # Kolom Data
    kode_barang = db.Column(db.String(50), unique=True, nullable=False)
    nama_barang = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.Text, nullable=True) # Merupakan Keterangan
    jumlah = db.Column(db.Integer, nullable=False)
    kondisi = db.Column(db.String(50), nullable=False)
    lokasi = db.Column(db.String(100), nullable=True)
    tanggal_masuk = db.Column(db.Date, nullable=False, default=lambda: datetime.now(timezone.utc).date())
    
    # Timestamps
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships using back_populates
    kategori = db.relationship('Kategori', back_populates='barang_inventaris')
    admin = db.relationship('Admin', back_populates='barang_inventaris')

    # Constraints (Validasi pada level database)
    __table_args__ = (
        CheckConstraint('jumlah >= 0', name='check_jumlah_positif'),
        CheckConstraint("kondisi IN ('Baik', 'Rusak Ringan', 'Rusak Berat')", name='check_kondisi_valid'),
    )
