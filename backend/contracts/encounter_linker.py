"""
Clinical Encounter Context Synchronizer for Member 3 (EMR Encounters).
Enriches diagnostic orders with encounter class (inpatient, outpatient, emergency),
bed location, and attending provider ID.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class ClinicalEncounterContext:
    encounter_id: str
    encounter_class: str  # INPATIENT, OUTPATIENT, EMERGENCY, ICU
    assigned_bed: Optional[str]
    attending_physician_id: str
    chief_complaint: str

class EncounterContextLinker:
    @staticmethod
    def link_order_to_encounter(order_dict: Dict[str, Any], context: ClinicalEncounterContext) -> Dict[str, Any]:
        enriched = order_dict.copy()
        enriched["encounter_id"] = context.encounter_id
        enriched["encounter_class"] = context.encounter_class
        enriched["bed_location"] = context.assigned_bed
        enriched["attending_physician_id"] = context.attending_physician_id
        return enriched
