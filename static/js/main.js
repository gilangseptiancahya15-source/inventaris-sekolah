/**
 * main.js - Vanilla JavaScript
 * Mengatur interaktivitas global aplikasi SIM Inventaris Sekolah.
 */

document.addEventListener("DOMContentLoaded", function () {

    // ─── 1. Page Loader ──────────────────────────────────────────
    const pageLoader = document.getElementById('page-loader');
    if (pageLoader) {
        pageLoader.style.opacity = '0';
        setTimeout(() => { pageLoader.style.display = 'none'; }, 400);
    }

    // ─── 2. Auto Hide Flash Messages (hilang setelah 5 detik) ────
    const flashAlerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    flashAlerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = "opacity 0.5s ease, margin 0.5s ease, padding 0.5s ease";
            alert.style.opacity = "0";
            setTimeout(() => { if (alert.parentNode) alert.remove(); }, 500);
        }, 5000);
    });

    // ─── 3. Form Validation (Bootstrap Integration) ───────────────
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                // Tampilkan loader saat form disubmit (kecuali form 'no-loader')
                if (pageLoader && !form.classList.contains('no-loader')) {
                    pageLoader.style.display = 'flex';
                    setTimeout(() => { pageLoader.style.opacity = '1'; }, 10);
                }
            }
            form.classList.add('was-validated');
        }, false);
    });

    // ─── 4. Confirm Delete ────────────────────────────────────────
    const deleteLinks = document.querySelectorAll('.confirm-delete');
    deleteLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            const pesan = this.getAttribute('data-confirm-message') || 'Apakah Anda yakin ingin menghapus data ini secara permanen?';
            if (!confirm(pesan)) {
                e.preventDefault();
            }
        });
    });

    // ─── 5. Bootstrap Tooltip Initialization ─────────────────────
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[title], [data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (el) {
        if (!el.hasAttribute('data-bs-original-title')) {
            return new bootstrap.Tooltip(el, { trigger: 'hover' });
        }
    });

    // ─── 6. Sidebar Active Link Auto-detection (Fallback JS) ──────
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    const hasActiveJinja = document.querySelector('.sidebar .nav-link.active');
    if (!hasActiveJinja) {
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && href !== '#') {
                if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
                    link.classList.add('active');
                }
            }
        });
    }

    // ─── 7. Sidebar Mobile Toggle ─────────────────────────────────
    const sidebarMenu = document.getElementById('sidebarMenu');
    const mainContent = document.querySelector('main');
    if (sidebarMenu && mainContent) {
        mainContent.addEventListener('click', () => {
            if (window.innerWidth < 768 && sidebarMenu.classList.contains('show')) {
                const bsCollapse = bootstrap.Collapse.getInstance(sidebarMenu);
                if (bsCollapse) bsCollapse.hide();
            }
        });
    }

    // ─── 8. Counter Animation (untuk publik/statistik) ───────────
    function animateCounter(el) {
        const target = parseInt(el.getAttribute('data-target'), 10) || 0;
        if (target === 0) { el.textContent = '0'; return; }
        const duration = 1000;
        const increment = Math.ceil(target / (duration / 16));
        let current = 0;
        const timer = setInterval(() => {
            current = Math.min(current + increment, target);
            el.textContent = current.toLocaleString('id-ID');
            if (current >= target) clearInterval(timer);
        }, 16);
    }

    const counterEls = document.querySelectorAll('.counter[data-target]');
    if (counterEls.length > 0) {
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

    // ─── 9. Navbar publik — active link ───────────────────────────
    const pubNavLinks = document.querySelectorAll('#navbarPublic .nav-link');
    pubNavLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href && window.location.pathname === href) {
            link.classList.add('fw-bold', 'text-primary');
        }
    });

    // Catatan: Inisialisasi Chart.js dipindahkan ke inline script di masing-masing template 
    // (home.html & statistik.html) untuk memastikan chart ter-render dengan benar di production / Vercel
    // dan tidak terpengaruh oleh isu caching pada file main.js.

}); // end DOMContentLoaded
