"""
ACR RADPEER Radiology Peer Review and Quality Assurance Logger.
Implements standardized double-reading and diagnostic discrepancy scoring.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class PeerReviewScore:
    score: int
    concurrence_type: str
    clinical_significance: str

class RadiologyPeerReviewEngine:
    RADPEER_SCORES = {
        1: PeerReviewScore(1, "Concur with Interpretation", "None"),
        2: PeerReviewScore(2, "Discrepancy: Understandable Difference of Opinion", "Not Clinically Significant"),
        3: PeerReviewScore(3, "Discrepancy: Variance in Interpretation", "Not Clinically Significant"),
        4: PeerReviewScore(4, "Discrepancy: Variance in Interpretation", "Clinically Significant")
    }

    @classmethod
    def evaluate_score(cls, score: int) -> PeerReviewScore:
        return cls.RADPEER_SCORES.get(score, cls.RADPEER_SCORES[1])
