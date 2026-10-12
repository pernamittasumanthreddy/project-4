import pytest
from clinical.services.vitals_mews_calculator import MEWSCalculatorService

def test_vitals_mews_calculator():
    res = MEWSCalculatorService.compute_mews("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
