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

    // 8. Animasi Counter (untuk halaman publik: statistik card)
    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'), 10) || 0;
        const duration = 1200; // ms
        const step = Math.ceil(duration / (target || 1));
        let current = 0;
        const timer = setInterval(() => {
            current += Math.ceil(target / (duration / 16));
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = current.toLocaleString('id-ID');
        }, 16);
    }

    const counterEls = document.querySelectorAll('.counter[data-target]');
    if (counterEls.length > 0) {
        // Gunakan Intersection Observer agar animasi mulai saat elemen terlihat layar
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.dataset.animated) {
                    entry.target.dataset.animated = 'true';
                    animateCounter(entry.target);
                }
            });
        }, { threshold: 0.5 });
        counterEls.forEach(el => observer.observe(el));
    }

    // 9. Aktifkan nav link publik berdasarkan URL aktif
    const pubNavLinks = document.querySelectorAll('#navbarPublic .nav-link');
    pubNavLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && window.location.pathname === href) {
            link.classList.add('text-primary', 'fw-bold');
        }
    });

    // 10. Inisialisasi Chart.js untuk halaman publik (home & statistik)
    // Grafik Kategori Publik (Home Page - Bar Chart)
    const kategoriPublicCtx = document.getElementById('kategoriPublicChart');
    if (kategoriPublicCtx && typeof kategoriLabel !== 'undefined') {
        new Chart(kategoriPublicCtx, {
            type: 'bar',
            data: {
                labels: kategoriLabel,
                datasets: [{
                    label: 'Jumlah Barang',
                    data: kategoriData,
                    backgroundColor: 'rgba(13, 110, 253, 0.75)',
                    borderColor: 'rgba(13, 110, 253, 1)',
                    borderWidth: 2,
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#f0f0f0' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    // Grafik Kondisi Publik (Home Page - Doughnut Chart)
    const kondisiPublicCtx = document.getElementById('kondisiPublicChart');
    if (kondisiPublicCtx && typeof kondisiLabel !== 'undefined') {
        new Chart(kondisiPublicCtx, {
            type: 'doughnut',
            data: {
                labels: kondisiLabel,
                datasets: [{
                    data: kondisiData,
                    backgroundColor: ['#198754', '#ffc107', '#dc3545'],
                    borderColor: ['#fff', '#fff', '#fff'],
                    borderWidth: 3,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                cutout: '65%',
                plugins: {
                    legend: { position: 'bottom', labels: { padding: 20, usePointStyle: true } }
                }
            }
        });
    }

    // Grafik Kategori Statistik Page (Bar Chart - horizontal feel)
    const kategoriBarCtx = document.getElementById('kategoriBarChart');
    if (kategoriBarCtx && typeof kategoriLabel !== 'undefined') {
        new Chart(kategoriBarCtx, {
            type: 'bar',
            data: {
                labels: kategoriLabel,
                datasets: [{
                    label: 'Jumlah Barang',
                    data: kategoriData,
                    backgroundColor: kategoriData.map((_, i) => `hsl(${210 + i * 30}, 70%, 55%)`),
                    borderRadius: 8,
                    borderSkipped: false,
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#f0f0f0' } },
                    y: { grid: { display: false } }
                }
            }
        });
    }

    // Grafik Kondisi Statistik Page (Doughnut Chart)
    const kondisiDoughnutCtx = document.getElementById('kondisiDoughnutChart');
    if (kondisiDoughnutCtx && typeof kondisiLabel !== 'undefined') {
        new Chart(kondisiDoughnutCtx, {
            type: 'doughnut',
            data: {
                labels: kondisiLabel,
                datasets: [{
                    data: kondisiData,
                    backgroundColor: ['#198754', '#ffc107', '#dc3545'],
                    borderColor: ['#fff', '#fff', '#fff'],
                    borderWidth: 3,
                    hoverOffset: 6
                }]
            },
            options: {
                responsive: true,
                cutout: '65%',
                plugins: { legend: { display: false } }
            }
        });
    }
});
