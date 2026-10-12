"""
Radiology Radiation Safety and Patient Cumulative Dose Monitoring.
Monitors Computed Tomography Dose Index (CTDIvol) and Dose Length Product (DLP)
against AAPM / ACR Diagnostic Reference Levels (DRLs).
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CTDoseRecord:
    modality_id: str
    study_instance_uid: str
    body_part_examined: str
    ctdi_vol_mgy: float
    dlp_mgy_cm: float
    total_exposure_time_sec: float

class RadiationDoseMonitor:
    # AAPM Diagnostic Reference Levels for standard adult phantom
    DRL_THRESHOLDS: Dict[str, Dict[str, float]] = {
        "HEAD": {"ctdi_max": 75.0, "dlp_max": 1050.0},
        "CHEST": {"ctdi_max": 21.0, "dlp_max": 650.0},
        "ABDOMEN_PELVIS": {"ctdi_max": 25.0, "dlp_max": 780.0}
    }

    @classmethod
    def check_dose_exceedance(cls, body_part: str, ctdi: float, dlp: float) -> Dict[str, Any]:
        key = body_part.upper().replace(" ", "_")
        limits = cls.DRL_THRESHOLDS.get(key, {"ctdi_max": 50.0, "dlp_max": 1000.0})
        exceeds_ctdi = ctdi > limits["ctdi_max"]
        exceeds_dlp = dlp > limits["dlp_max"]
        return {
            "exceeds_drl": exceeds_ctdi or exceeds_dlp,
            "ctdi_ratio": round(ctdi / limits["ctdi_max"], 2),
            "dlp_ratio": round(dlp / limits["dlp_max"], 2)
        }
