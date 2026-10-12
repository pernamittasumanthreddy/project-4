import pytest
from clinical.services.erx_dispense_lifecycle import ERxDispenseLifecycle

def test_erx_dispense_lifecycle():
    res = ERxDispenseLifecycle.transition_dispense_state("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
