from admissions.clearance_service import DischargeClearanceService

def test_clearance_verification():
    res1 = DischargeClearanceService.verify_all_clearances(True, True, True)
    assert res1["is_discharge_ready"] is True
    res2 = DischargeClearanceService.verify_all_clearances(True, False, True)
    assert res2["is_discharge_ready"] is False
