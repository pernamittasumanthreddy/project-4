import pytest
from clinical.services.discharge_med_reconciliation import DischargeMedReconciliation

def test_discharge_med_reconciliation():
    res = DischargeMedReconciliation.reconcile_medications("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
