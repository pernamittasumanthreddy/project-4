import pytest
from clinical.services.erx_builder_service import ERxBuilderService

def test_erx_builder_service():
    res = ERxBuilderService.build_erx_order("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
