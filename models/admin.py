import uuid
from datetime import datetime, timezone
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Admin(db.Model):
    __tablename__ = 'admin'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(255), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Timestamp
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationship using back_populates
    barang_inventaris = db.relationship('BarangInventaris', back_populates='admin', lazy=True)

    # Password Hashing Methods
    def set_password(self, password):
        """Menghasilkan hash dari password raw dan menyimpannya ke password_hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Mengecek kecocokan password raw dengan hash yang ada di database."""
        return check_password_hash(self.password_hash, password)
