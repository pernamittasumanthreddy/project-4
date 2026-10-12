import pytest
from clinical.services.pediatric_dosing_calculator import PediatricDosingCalculator

def test_pediatric_dosing_calculator():
    res = PediatricDosingCalculator.check_pediatric_bounds("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
