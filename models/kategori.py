import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from app import db

class Kategori(db.Model):
    __tablename__ = 'kategori'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nama_kategori = db.Column(db.String(100), unique=True, nullable=False)
    deskripsi = db.Column(db.Text, nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationship using back_populates
    barang_inventaris = db.relationship('BarangInventaris', back_populates='kategori', lazy=True)
