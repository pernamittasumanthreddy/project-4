import pytest
from clinical.services.prescription_barcode_labeler import PrescriptionBarcodeLabeler

def test_prescription_barcode_labeler():
    res = PrescriptionBarcodeLabeler.generate_label("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
