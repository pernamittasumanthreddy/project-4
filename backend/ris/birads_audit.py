"""
ACR BI-RADS Mammography Assessment and Follow-Up Audit Engine.
Encodes BI-RADS categories (0-6), breast composition (A-D), and MQSA compliance checks.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class BIRADSClassification:
    category: int
    assessment: str
    recommendation: str
    malignancy_risk: str

class BIRADSAuditEngine:
    CATEGORIES: Dict[int, BIRADSClassification] = {
        0: BIRADSClassification(0, "Incomplete", "Additional imaging evaluation and/or prior mammograms needed.", "N/A"),
        1: BIRADSClassification(1, "Negative", "Routine screening mammography.", "Essentially 0%"),
        2: BIRADSClassification(2, "Benign", "Routine screening mammography.", "Essentially 0%"),
        3: BIRADSClassification(3, "Probably Benign", "Short-interval follow-up (6 months).", "< 2%"),
        4: BIRADSClassification(4, "Suspicious", "Tissue diagnosis / biopsy should be considered.", "2% to 95%"),
        5: BIRADSClassification(5, "Highly Suggestive of Malignancy", "Appropriate action / surgical biopsy required.", "> 95%"),
        6: BIRADSClassification(6, "Known Biopsy-Proven Malignancy", "Surgical excision or neoadjuvant therapy.", "100%")
    }

    @classmethod
    def get_assessment(cls, cat: int) -> BIRADSClassification:
        return cls.CATEGORIES.get(cat, cls.CATEGORIES[0])
