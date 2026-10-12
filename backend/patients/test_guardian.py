from patients.guardian_service import GuardianProxyService

def test_minor_proxy():
    assert GuardianProxyService.verify_minor_representation(10, "PARENT") is True
    assert GuardianProxyService.verify_minor_representation(10, "FRIEND") is False
    assert GuardianProxyService.verify_minor_representation(25, "FRIEND") is True
