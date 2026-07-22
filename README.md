# Aplikasi Inventaris Sekolah

Aplikasi Web Inventaris Sekolah yang dibangun menggunakan framework **Flask (Python)**. Aplikasi ini dirancang untuk memudahkan pihak sekolah dalam mendata, mengelola, dan memantau kondisi barang-barang inventaris yang ada di lingkungan sekolah.

## Fitur Utama ✨

- **Autentikasi Aman:** Sistem login khusus untuk Admin (menggunakan dekorator `@login_required`).
- **Dashboard Interaktif:** Menampilkan ringkasan statistik seperti total kategori, total barang, serta rincian kondisi barang (Baik, Rusak Ringan, Rusak Berat), dan aktivitas terbaru.
- **Manajemen Kategori:** Tambah, edit, dan hapus kategori barang inventaris.
- **Manajemen Barang:** Pencatatan detail barang termasuk jumlah, kondisi, dan kategori.
- **Laporan (Laporan):** Cetak/lihat laporan data inventaris barang secara keseluruhan.
- **Error Handling:** Halaman khusus untuk error 404 (Not Found), 500 (Internal Server Error), dan pembatasan ukuran file (413).

## Teknologi yang Digunakan 🛠️

- **Backend:** Python 3, Flask 3.0
- **Database:** PostgreSQL (didukung oleh `psycopg2-binary`)
- **ORM & Migrasi:** Flask-SQLAlchemy, Flask-Migrate
- **Deployment:** Vercel (mendukung `vercel.json` dan variabel lingkungan)
- **Frontend:** HTML, CSS, JavaScript (menggunakan Chart.js untuk grafik)

## Prasyarat (Prerequisites) 📋

Pastikan Anda telah menginstal perangkat lunak berikut sebelum memulai:
- [Python 3.8+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/downloads)

## Instalasi dan Menjalankan di Lokal 🚀

Ikuti langkah-langkah di bawah ini untuk menjalankan aplikasi di komputer lokal Anda.

### 1. Clone Repositori
```bash
git clone https://github.com/username-anda/inventaris-sekolah.git
cd inventaris-sekolah
```

### 2. Buat Virtual Environment & Aktivasi
Disarankan menggunakan Virtual Environment untuk mengisolasi dependensi aplikasi.
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Variabel Lingkungan
Buat file bernama `.env` di direktori utama proyek, lalu isi dengan konfigurasi database Anda. Contoh isi `.env`:
```env
# Ganti dengan URI database PostgreSQL Anda
SQLALCHEMY_DATABASE_URI=postgresql://postgres:password_anda@localhost:5432/inventaris_db
SECRET_KEY=rahasia-super-aman
```
> **Catatan:** Pastikan database `inventaris_db` sudah dibuat di PostgreSQL Anda.

### 5. Inisialisasi Database (Migrasi)
Jalankan perintah berikut untuk membuat tabel di database:
```bash
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

### 6. Buat Akun Admin (Seeding)
Jalankan skrip seed untuk membuat akun admin default.
```bash
python seed_admin.py
```
Setelah berhasil dijalankan, Anda dapat login dengan kredensial berikut:
- **Email:** `admin@inventaris.com`
- **Password:** `password123`

### 7. Jalankan Aplikasi
```bash
python app.py
```
Aplikasi akan berjalan di `http://127.0.0.1:5000`. Silakan buka browser Anda dan login.

## Deployment ke Vercel ☁️

Aplikasi ini sudah disesuaikan agar mudah di-deploy ke Vercel. 
1. Pastikan file `vercel.json` sudah ada di *root directory*.
2. Hubungkan repositori GitHub Anda ke project Vercel.
3. Masuk ke tab **Settings > Environment Variables** di dashboard Vercel.
4. Tambahkan `DATABASE_URL` (berisi link PostgreSQL Anda, misal dari Supabase/Neon) dan `SECRET_KEY`.
5. Deploy project.

## Struktur Direktori 📁
```
inventaris-sekolah/
│
├── models/             # Definisi tabel Database (Admin, Kategori, Barang)
├── routes/             # Blueprints routing (auth, kategori, barang, laporan, public)
├── templates/          # File HTML (Jinja2)
├── static/             # CSS, JS, dan Gambar statis
├── utils/              # Fungsi bantuan (seperti decorators)
├── app.py              # Entry point aplikasi Flask
├── config.py           # File konfigurasi aplikasi
├── seed_admin.py       # Skrip untuk inisiasi akun admin
├── requirements.txt    # Daftar dependensi library Python
└── vercel.json         # Konfigurasi deployment Vercel
```

## Lisensi 📄
Proyek ini dibuat untuk keperluan pembelajaran/tugas (*Pengantar Pemrograman*). Silakan gunakan dan modifikasi sesuai kebutuhan.
