from admissions.policy_service import BedPolicyService

def test_policy():
    expired = BedPolicyService.evaluate_reservation_timeout(2, 3)
    assert expired is True
