import pytest
from clinical.services.integrity_service import ClinicalIntegrityService

def test_integrity_service():
    res = ClinicalIntegrityService.verify_digest("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
