import pytest
from clinical.services.code_status_directive import CodeStatusDirective

def test_code_status_directive():
    res = CodeStatusDirective.validate_code_status("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
