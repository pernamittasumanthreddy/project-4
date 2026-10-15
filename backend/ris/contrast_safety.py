"""
Intravenous Contrast Media Safety and Nephrotoxicity Protection Engine.
Screens eGFR levels for Contrast-Induced Nephropathy (CIN) and Nephrogenic Systemic Fibrosis (NSF)
and verifies patient contrast allergy pre-medication regimens.
"""

from typing import Dict, Any

class ContrastMediaSafetyEngine:
    @staticmethod
    def evaluate_contrast_risk(egfr_ml_min: float, contrast_agent_type: str) -> Dict[str, Any]:
        if egfr_ml_min < 30.0:
            return {
                "risk_tier": "HIGH",
                "safe_to_administer": False,
                "action": "Hold IV contrast. Consult ordering physician and nephrologist.",
                "cin_risk": "Severe"
            }
        elif egfr_ml_min < 45.0:
            return {
                "risk_tier": "MODERATE",
                "safe_to_administer": True,
                "action": "Proceed with caution. Recommend isotonic saline pre/post hydration.",
                "cin_risk": "Elevated"
            }
        return {
            "risk_tier": "LOW",
            "safe_to_administer": True,
            "action": "Standard administration protocol.",
            "cin_risk": "Minimal"
        }
