import pytest
from clinical.services.amendment_service import ClinicalAmendmentService

def test_amendment_service():
    res = ClinicalAmendmentService.track_addendum("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
