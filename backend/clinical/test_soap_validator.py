import pytest
from clinical.services.soap_validator import SOAPValidationService

def test_soap_validator():
    res = SOAPValidationService.validate_encounter("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
