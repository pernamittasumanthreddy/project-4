"""
Drug-Laboratory Test Analytical Interference Knowledge Base for Member 5 (Pharmacy).
Alerts phlebotomists and pathologists to pharmaceutical agents distorting lab assays.
"""

from typing import Dict, List, Any

class DrugLabInterferenceMatrix:
    KNOWN_INTERFERENCES = {
        "BIOTIN": [
            {"test_code": "TSH", "effect": "FALSE_LOW", "mechanism": "Streptavidin-biotin immunoassays interference"},
            {"test_code": "TROPONIN_I", "effect": "FALSE_LOW", "mechanism": "Immunoassay binding interference"},
            {"test_code": "FT4", "effect": "FALSE_HIGH", "mechanism": "Competitive binding displacement"}
        ],
        "HEPARIN": [
            {"test_code": "PT_INR", "effect": "PROLONGED", "mechanism": "Inhibition of coagulation cascade enzymes"},
            {"test_code": "APTT", "effect": "PROLONGED", "mechanism": "Factor Xa and Thrombin inhibition"}
        ],
        "CEFTRIAXONE": [
            {"test_code": "DIRECT_COOMBS", "effect": "FALSE_POSITIVE", "mechanism": "Non-immunologic protein adsorption"}
        ]
    }

    @classmethod
    def check_active_medications(cls, test_code: str, active_meds: List[str]) -> List[Dict[str, Any]]:
        alerts = []
        for med in active_meds:
            med_key = med.upper().strip()
            if med_key in cls.KNOWN_INTERFERENCES:
                for rule in cls.KNOWN_INTERFERENCES[med_key]:
                    if rule["test_code"] == test_code.upper():
                        alerts.append({"medication": med_key, **rule})
        return alerts
