/**
 * Bedside Phlebotomy Offline Collection Manager (IndexedDB / LocalStorage).
 * Buffers tube collection events during temporary hospital Wi-Fi dead-zones.
 */
class PhlebotomyOfflineCache {
    static STORAGE_KEY = 'HMS_BEDSIDE_PENDING_DRAWS';

    static savePendingDraw(accessionNumber, tubeBarcode, collectedAt) {
        const queue = this.getPendingDraws();
        queue.push({ accessionNumber, tubeBarcode, collectedAt });
        localStorage.setItem(this.STORAGE_KEY, JSON.stringify(queue));
    }

    static getPendingDraws() {
        try {
            return JSON.parse(localStorage.getItem(this.STORAGE_KEY) || '[]');
        } catch (e) {
            return [];
        }
    }

    static clearCache() {
        localStorage.removeItem(this.STORAGE_KEY);
    }
}
window.PhlebotomyOfflineCache = PhlebotomyOfflineCache;
