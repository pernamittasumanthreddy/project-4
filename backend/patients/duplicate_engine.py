import difflib
from typing import List, Dict, Any
from patients.models import Patient


class PatientDuplicateEngine:
    """
    Algorithmic duplicate detection engine combining exact matching,
    fuzzy string distance, and demographic similarity weighting.
    """

    @staticmethod
    def calculate_similarity(s1: str, s2: str) -> float:
        if not s1 or not s2:
            return 0.0
        return difflib.SequenceMatcher(None, s1.strip().lower(), s2.strip().lower()).ratio()

    @classmethod
    def scan_for_duplicates(
        cls,
        tenant_id,
        first_name: str,
        last_name: str,
        phone: str,
        date_of_birth=None,
        national_id: str = "",
        exclude_patient_id=None,
        threshold: float = 0.65
    ) -> List[Dict[str, Any]]:
        """
        Scans existing active patients in the tenant and returns potential matches with confidence scores.
        """
        qs = Patient.objects.filter(
            tenant_id=tenant_id,
            is_deleted=False,
            is_merged=False
        )

        if exclude_patient_id:
            qs = qs.exclude(id=exclude_patient_id)

        candidates = []

        for p in qs[:200]:  # Cap scan batch for optimal latency
            score = 0.0
            reasons = []

            # Exact National ID match (100% certainty)
            if national_id and p.national_id and national_id.strip() == p.national_id.strip():
                score = 1.0
                reasons.append("Exact National ID match")
                candidates.append({
                    "patient_id": str(p.id),
                    "mrn": p.mrn,
                    "full_name": p.full_name,
                    "phone": p.phone,
                    "date_of_birth": str(p.date_of_birth) if p.date_of_birth else None,
                    "national_id": p.national_id,
                    "confidence_score": round(score, 2),
                    "match_reasons": reasons,
                })
                continue

            # Phone match (Weight: 0.40)
            if phone and p.phone and phone.strip() == p.phone.strip():
                score += 0.40
                reasons.append("Identical contact phone number")

            # Name similarity (Weight: 0.35)
            first_sim = cls.calculate_similarity(first_name, p.first_name)
            last_sim = cls.calculate_similarity(last_name, p.last_name)
            name_score = (first_sim * 0.20) + (last_sim * 0.15)
            if name_score > 0.25:
                score += name_score
                reasons.append(f"Name similarity (First: {int(first_sim*100)}%, Last: {int(last_sim*100)}%)")

            # Date of Birth match (Weight: 0.25)
            if date_of_birth and p.date_of_birth and str(date_of_birth) == str(p.date_of_birth):
                score += 0.25
                reasons.append("Exact Date of Birth match")

            if score >= threshold:
                candidates.append({
                    "patient_id": str(p.id),
                    "mrn": p.mrn,
                    "full_name": p.full_name,
                    "phone": p.phone,
                    "date_of_birth": str(p.date_of_birth) if p.date_of_birth else None,
                    "national_id": p.national_id,
                    "confidence_score": round(min(score, 1.0), 2),
                    "match_reasons": reasons,
                })

        candidates.sort(key=lambda x: x["confidence_score"], reverse=True)
        return candidates

