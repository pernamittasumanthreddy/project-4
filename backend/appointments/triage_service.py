class OPDPriorityTriageService:
    @staticmethod
    def calculate_priority_score(age, is_emergency=False, pain_score=0):
        score = 0
        if is_emergency:
            score += 100
        if age is not None and (age < 5 or age > 70):
            score += 30
        score += min(pain_score * 5, 50)
        return score
