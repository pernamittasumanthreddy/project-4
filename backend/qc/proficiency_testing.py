"""
External Quality Assessment (EQA) and Proficiency Testing (PT) Evaluator.
Computes Standard Deviation Index (SDI) and Z-Scores against peer-group survey means.
"""

from typing import Dict, Any

class ProficiencyTestingTracker:
    @staticmethod
    def calculate_sdi(lab_result: float, peer_group_mean: float, peer_group_sd: float) -> Dict[str, Any]:
        if peer_group_sd <= 0:
            return {"sdi": 0.0, "performance": "UNACCEPTABLE_SD_ZERO"}
        sdi = (lab_result - peer_group_mean) / peer_group_sd
        
        perf = "ACCEPTABLE"
        if abs(sdi) > 3.0:
            perf = "UNACCEPTABLE"
        elif abs(sdi) > 2.0:
            perf = "QUESTIONABLE"
            
        return {
            "sdi": round(sdi, 2),
            "z_score": round(sdi, 2),
            "performance": perf
        }
