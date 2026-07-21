from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import Admin

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Jika admin sudah login, tidak perlu login lagi, langsung arahkan ke index/dashboard
    if 'admin_id' in session:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Mencari admin berdasarkan email
        admin = Admin.query.filter_by(email=email).first()

        # Verifikasi password hash menggunakan method check_password dari model
        if admin and admin.check_password(password):
            # Set variabel session agar user tetap 'logged in' di setiap halaman
            session['admin_id'] = str(admin.id)
            session['admin_nama'] = admin.nama
            session['admin_email'] = admin.email
            
            # Buat Flash Message untuk notifikasi sukses
            flash("Berhasil login! Selamat datang, " + admin.nama, "success")
            return redirect(url_for('dashboard'))
        else:
            # Flash Message untuk notifikasi error
            flash("Email atau password yang Anda masukkan salah.", "danger")
            return redirect(url_for('auth.login'))

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    # Menghapus seluruh data dari session
    session.clear()
    flash("Anda telah berhasil logout.", "info")
    return redirect(url_for('auth.login'))
