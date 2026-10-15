"""
Automated Unit Tests for LIS Specimen Cold-Chain Temperature Telemetry.
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from lis.specimen_temperature_telemetry import SpecimenTemperatureValidator

def test_refrigerated_specimen_optimal():
    res = SpecimenTemperatureValidator.evaluate_telemetry("REFRIGERATED", recorded_temp=4.5)
    assert res["is_compliant"] is True
    assert res["status"] == "OPTIMAL"
    assert res["recommended_action"] == "PROCESS_SAMPLE"

def test_refrigerated_specimen_transient_excursion():
    res = SpecimenTemperatureValidator.evaluate_telemetry("REFRIGERATED", recorded_temp=9.2, excursion_duration_min=15)
    assert res["is_compliant"] is False
    assert res["status"] == "TRANSIENT_EXCURSION"
    assert res["recommended_action"] == "ACCEPT_WITH_CAUTION"

def test_refrigerated_specimen_critical_excursion():
    res = SpecimenTemperatureValidator.evaluate_telemetry("REFRIGERATED", recorded_temp=12.0, excursion_duration_min=45)
    assert res["is_compliant"] is False
    assert res["status"] == "CRITICAL_EXCURSION"
    assert res["recommended_action"] == "REJECT_SPECIMEN"

def test_frozen_specimen_compliant():
    res = SpecimenTemperatureValidator.evaluate_telemetry("FROZEN", recorded_temp=-25.0)
    assert res["is_compliant"] is True
    assert res["status"] == "OPTIMAL"

def test_unknown_storage_category():
    res = SpecimenTemperatureValidator.evaluate_telemetry("ULTRA_WARM", recorded_temp=37.0)
    assert res["is_compliant"] is False
    assert res["status"] == "UNKNOWN_STORAGE_CATEGORY"
    assert res["recommended_action"] == "REJECT_SPECIMEN"

if __name__ == "__main__":
    test_refrigerated_specimen_optimal()
    test_refrigerated_specimen_transient_excursion()
    test_refrigerated_specimen_critical_excursion()
    test_frozen_specimen_compliant()
    test_unknown_storage_category()
    print("All specimen temperature telemetry tests passed successfully!")
