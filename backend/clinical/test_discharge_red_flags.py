import pytest
from clinical.services.discharge_red_flags import DischargeRedFlagGenerator

def test_discharge_red_flags():
    res = DischargeRedFlagGenerator.generate_warnings("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
