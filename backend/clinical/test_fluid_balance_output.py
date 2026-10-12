import pytest
from clinical.services.fluid_balance_output import FluidOutputCalculator

def test_fluid_balance_output():
    res = FluidOutputCalculator.calculate_output("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
