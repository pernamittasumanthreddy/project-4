import pytest
from clinical.services.antimicrobial_stewardship import AntimicrobialStewardshipAdvisor

def test_antimicrobial_stewardship():
    res = AntimicrobialStewardshipAdvisor.advise_deescalation("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
