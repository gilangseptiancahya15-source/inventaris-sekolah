/**
 * main.js - Vanilla JavaScript File
 * Mengatur interaktivitas global aplikasi (DOM Manipulation)
 */

document.addEventListener("DOMContentLoaded", function () {
    
    // 1. Loading Spinner & Skeleton UI (Transisi Halus)
    setTimeout(function() {
        const skeleton = document.getElementById('skeleton-container');
        const content = document.getElementById('actual-content');
        
        if (skeleton) skeleton.style.display = 'none';
        if (content) content.style.opacity = '1';
        
        const pageLoader = document.getElementById('page-loader');
        if (pageLoader) {
            pageLoader.style.opacity = '0';
            setTimeout(() => pageLoader.style.display = 'none', 400); // 400ms sesuai durasi transisi CSS
        }
    }, 400); // Menunda sedikit untuk estetika skeleton

    // 2. Auto Hide Flash Message (Hilang dalam 5 Detik)
    const flashAlerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    flashAlerts.forEach(alert => {
        setTimeout(() => {
            // Animasi fade-out murni JavaScript
            alert.style.transition = "opacity 0.5s ease, margin 0.5s ease, padding 0.5s ease, height 0.5s ease";
            alert.style.opacity = "0";
            
            // Tunggu animasi selesai lalu hapus elemen dari DOM
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // 3. Form Validation (Bootstrap Class Integration) & Show Spinner
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        // Menonaktifkan pop-up tooltip validasi bawaan browser (Opsional, agar murni style Bootstrap)
        // form.setAttribute('novalidate', ''); 

        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                // Jika tidak valid, cegah pengiriman form
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Tampilkan loading spinner jika form valid (menandakan proses ke server)
                const pageLoader = document.getElementById('page-loader');
                // Jika form memiliki class 'no-loader' (seperti search form sederhana), abaikan spinner
                if (pageLoader && !form.classList.contains('no-loader')) {
                    pageLoader.style.display = 'flex';
                    setTimeout(() => pageLoader.style.opacity = '1', 10);
                }
            }
            
            // Tambahkan class 'was-validated' dari Bootstrap untuk memunculkan indikator warna merah/hijau
            form.classList.add('was-validated');
        }, false);
    });

    // 4. Confirm Delete (Generic Class Handler)
    // Jika ada elemen dengan class 'confirm-delete', ia akan meminta konfirmasi JS Alert sebelum lanjut
    const deleteLinks = document.querySelectorAll('.confirm-delete');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const pesan = this.getAttribute('data-confirm-message') || 'Apakah Anda yakin ingin menghapus data ini secara permanen?';
            if (!confirm(pesan)) {
                e.preventDefault();
            }
        });
    });

    // 5. Tooltip Bootstrap Initialization
    // Mengaktifkan seluruh elemen HTML yang memiliki title attribute
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title], [data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        // Jangan timpa jika tooltip sudah di-initialize oleh framework lain/Jinja
        if (!tooltipTriggerEl.hasAttribute('data-bs-original-title')) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        }
    });

    // 6. Navbar / Sidebar Active Auto-detection (Fallback JS)
    // Membaca URL di browser dan memberikan class 'active' ke menu sidebar yang sesuai
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    const hasActiveJinja = document.querySelector('.sidebar .nav-link.active');
    
    // Hanya dieksekusi jika Jinja tidak memberikan class active secara hardcode
    if (!hasActiveJinja) {
        navLinks.forEach(link => {
            const linkHref = link.getAttribute('href');
            if (linkHref && linkHref !== '#') {
                if (currentPath === linkHref || (linkHref !== '/' && currentPath.startsWith(linkHref))) {
                    link.classList.add('active');
                }
            }
        });
    }

    // 7. Sidebar Toggle (Mobile Auto-hide Overlay Enhancement)
    const sidebarMenu = document.getElementById('sidebarMenu');
    const mainContent = document.querySelector('main');
    
    if (sidebarMenu && mainContent) {
        // Jika layar di ukuran HP dan sidebar sedang terbuka, sentuhan di area luar sidebar akan menutupnya
        mainContent.addEventListener('click', () => {
            if (window.innerWidth < 768 && sidebarMenu.classList.contains('show')) {
                // Menggunakan API Bootstrap Collapse
                const bsCollapse = bootstrap.Collapse.getInstance(sidebarMenu);
                if (bsCollapse) bsCollapse.hide();
            }
        });
    }
});
