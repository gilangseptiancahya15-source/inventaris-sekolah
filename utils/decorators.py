from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """
    Decorator untuk memproteksi route (hanya bisa diakses jika user sudah login).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Jika 'admin_id' tidak ada di dalam session, tolak akses.
        if 'admin_id' not in session:
            flash("Silakan login terlebih dahulu untuk mengakses halaman ini.", "warning")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
