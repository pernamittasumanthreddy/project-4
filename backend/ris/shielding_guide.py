"""
NCRP Report No. 147 Structural Shielding Design Guide for Medical X-Ray Imaging Facilities.
"""
from typing import Dict

def get_recommended_lead_thickness_mm(modality: str) -> float:
    mod = modality.upper()
    if "CT" in mod:
        return 2.0  # 2.0 mm Lead equivalent
    elif "XRAY" in mod or "XR" in mod:
        return 1.5
    elif "MAMMO" in mod:
        return 0.5
    return 1.0
