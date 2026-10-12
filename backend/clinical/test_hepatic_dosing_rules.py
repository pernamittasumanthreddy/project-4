import pytest
from clinical.services.hepatic_dosing_rules import HepaticDosingRules

def test_hepatic_dosing_rules():
    res = HepaticDosingRules.get_hepatic_guidance("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
