"""
CLSI H1 / ISO 6710 Standard Tube Top Color and Anticoagulant Matrix.
"""
from typing import Dict, Any

TUBE_TOP_DICTIONARY: Dict[str, Dict[str, str]] = {
    "LAVENDER": {"additive": "K2 EDTA", "department": "Hematology", "inversions": "8-10"},
    "LIGHT_BLUE": {"additive": "3.2% Sodium Citrate", "department": "Coagulation", "inversions": "3-4"},
    "RED": {"additive": "Clot Activator", "department": "Serology", "inversions": "5"},
    "GOLD_SST": {"additive": "Clot Activator + Gel", "department": "Biochemistry", "inversions": "5"},
    "GREEN": {"additive": "Lithium Heparin", "department": "Stat Chemistry", "inversions": "8-10"},
    "GRAY": {"additive": "Sodium Fluoride / Potassium Oxalate", "department": "Glucose", "inversions": "8-10"}
}

def get_tube_specs(tube_color: str) -> Dict[str, str]:
    return TUBE_TOP_DICTIONARY.get(tube_color.upper(), {"additive": "None", "department": "General", "inversions": "5"})
