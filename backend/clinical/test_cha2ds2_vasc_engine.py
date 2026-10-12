import pytest
from clinical.services.cha2ds2_vasc_engine import CHA2DS2VAScEngine

def test_cha2ds2_vasc_engine():
    res = CHA2DS2VAScEngine.calculate_stroke_risk("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
