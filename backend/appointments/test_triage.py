from appointments.triage_service import OPDPriorityTriageService

def test_priority_score():
    score_er = OPDPriorityTriageService.calculate_priority_score(30, is_emergency=True)
    score_peds = OPDPriorityTriageService.calculate_priority_score(3, pain_score=8)
    assert score_er >= 100
    assert score_peds == 70
