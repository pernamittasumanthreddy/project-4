import pytest
from clinical.services.curb65_stratification import CURB65StratificationEngine

def test_curb65_stratification():
    res = CURB65StratificationEngine.evaluate_pneumonia_risk("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
