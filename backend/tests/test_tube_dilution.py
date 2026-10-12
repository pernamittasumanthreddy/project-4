"""Unit tests for Tube colors and dilution calculator."""
import pytest
from lis.tube_colors import get_tube_specs
from lis.dilution_calc import DilutionCalculator

def test_tube_colors():
    specs = get_tube_specs("LAVENDER")
    assert specs["department"] == "Hematology"
    assert "EDTA" in specs["additive"]

def test_dilution_calculator():
    calc = DilutionCalculator()
    res = calc.calculate_true_value(150.0, "1:5")
    assert res == 750.0
