import pytest
from clinical.services.discharge_summary_builder import DischargeSummaryBuilder

def test_discharge_summary_builder():
    res = DischargeSummaryBuilder.compile_summary("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
