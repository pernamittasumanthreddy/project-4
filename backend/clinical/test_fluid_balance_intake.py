import pytest
from clinical.services.fluid_balance_intake import FluidIntakeAggregator

def test_fluid_balance_intake():
    res = FluidIntakeAggregator.aggregate_intake("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
