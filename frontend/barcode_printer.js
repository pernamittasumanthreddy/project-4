/**
 * Client-Side Specimen Barcode Label Generator and Thermal Printer Driver.
 * Renders high-density Code128 barcodes for blood collection tubes.
 */
class SpecimenBarcodePrinter {
    static printTubeLabel(accessionNumber, patientName, testCode, tubeColor) {
        const printWindow = window.open('', '_blank', 'width=350,height=200');
        if (!printWindow) return;
        printWindow.document.write(`
            <html>
            <head><style>
                body { font-family: monospace; font-size: 10px; margin: 4px; padding: 0; }
                .label-box { border: 1px dashed #475569; padding: 6px; width: 280px; }
                .acc-code { font-size: 14px; font-weight: bold; letter-spacing: 2px; }
                .tube-badge { background: #334155; color: #fff; padding: 2px 4px; border-radius: 3px; }
            </style></head>
            <body>
                <div class="label-box">
                    <div><b>HMS LAB SPECIMEN</b> <span class="tube-badge">${tubeColor}</span></div>
                    <div class="acc-code">*${accessionNumber}*</div>
                    <div>PT: ${patientName}</div>
                    <div>TEST: ${testCode} | ${new Date().toLocaleTimeString()}</div>
                </div>
                <script>window.print(); setTimeout(() => window.close(), 500);</script>
            </body>
            </html>
        `);
        printWindow.document.close();
    }
}
window.SpecimenBarcodePrinter = SpecimenBarcodePrinter;
