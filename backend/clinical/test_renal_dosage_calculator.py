import pytest
from clinical.services.renal_dosage_calculator import RenalDosageCalculator

def test_renal_dosage_calculator():
    res = RenalDosageCalculator.calculate_renal_dose("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
