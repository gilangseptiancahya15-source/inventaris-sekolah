from app import create_app
from extensions import db
from models import Admin
from sqlalchemy.exc import OperationalError

print("Menghubungkan ke database...")

try:
    app = create_app()
    with app.app_context():
        # Memastikan tabel sudah dibuat
        db.create_all()
        
        # Mengecek apakah akun sudah pernah dibuat
        existing_admin = Admin.query.filter_by(email='admin@inventaris.com').first()
        
        if existing_admin:
            print("❌ Akun admin sudah ada di database.")
            print("Gunakan Email: admin@inventaris.com")
        else:
            # Membuat akun admin baru
            new_admin = Admin(
                nama='Administrator Utama',
                email='admin@inventaris.com'
            )
            new_admin.set_password('password123') # Password default
            
            db.session.add(new_admin)
            db.session.commit()
            
            print("✅ Akun Admin berhasil dibuat dengan sukses!")
            print("========================================")
            print("Email    : admin@inventaris.com")
            print("Password : password123")
            print("========================================")
            print("Silakan login menggunakan kredensial di atas.")

except OperationalError as e:
    print("\n❌ GAGAL TERHUBUNG KE DATABASE!")
    print("Pastikan Anda sudah memasukkan DATABASE_URL Supabase yang asli ke dalam file .env")
except Exception as e:
    print(f"\n❌ Terjadi kesalahan: {e}")
