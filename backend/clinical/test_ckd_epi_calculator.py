import pytest
from clinical.services.ckd_epi_calculator import CKDEPICalculator

def test_ckd_epi_calculator():
    res = CKDEPICalculator.compute_egfr("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
