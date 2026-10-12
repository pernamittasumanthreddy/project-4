/**
 * Clinical Keyboard Hotkeys and Rapid Access Navigation Controller.
 * Facilitates high-throughput phlebotomy, accessioning, and PACS viewing.
 */
document.addEventListener('keydown', (e) => {
    // Alt+N : Open New Lab Order
    if (e.altKey && (e.key === 'n' || e.key === 'N')) {
        e.preventDefault();
        const btn = document.getElementById('open-create-order-btn');
        if (btn) btn.click();
    }
    // Alt+R : Open New Radiology Order
    if (e.altKey && (e.key === 'r' || e.key === 'R')) {
        e.preventDefault();
        const btn = document.getElementById('open-create-imaging-btn');
        if (btn) btn.click();
    }
    // Escape : Close any open modals
    if (e.key === 'Escape') {
        const activeModal = document.querySelector('.modal-overlay.active');
        if (activeModal) activeModal.classList.remove('active');
    }
});
