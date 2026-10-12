import pytest
from clinical.services.immutability_guard import ImmutabilityGuard

def test_immutability_guard():
    res = ImmutabilityGuard.check_immutable("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
