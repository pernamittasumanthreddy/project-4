import pytest
from clinical.services.referral_lifecycle_service import ReferralLifecycleService

def test_referral_lifecycle_service():
    res = ReferralLifecycleService.dispatch_referral("test_input")
    assert res["status"] == "SUCCESS"
    assert res["result"] is True
