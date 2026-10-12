import pytest
from clinical.services.emar_rights_verification import EMARFiveRightsVerifier

def test_emar_rights_verification():
    res = EMARFiveRightsVerifier.verify_five_rights("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
