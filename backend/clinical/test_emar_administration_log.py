import pytest
from clinical.services.emar_administration_log import EMARAdministrationLogger

def test_emar_administration_log():
    res = EMARAdministrationLogger.log_administration("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
