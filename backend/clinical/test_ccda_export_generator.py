import pytest
from clinical.services.ccda_export_generator import CCDAExportGenerator

def test_ccda_export_generator():
    res = CCDAExportGenerator.export_ccda_document("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
