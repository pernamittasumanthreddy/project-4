"""
RSNA RadLex Standardized Radiology Terminology Mapper.
Maps anatomy and observation codes to RadLex RID identifiers.
"""

from typing import Dict, Optional

class RadLexTerminologyMapper:
    ANATOMY_MAP: Dict[str, str] = {
        "BRAIN": "RID41031",
        "CHEST": "RID1243",
        "LUNG": "RID1301",
        "LIVER": "RID58",
        "KIDNEY": "RID205",
        "LUMBAR_SPINE": "RID2616",
        "PELVIS": "RID2507"
    }

    FINDING_MAP: Dict[str, str] = {
        "PNEUMOTHORAX": "RID5270",
        "PULMONARY_EMBOLISM": "RID4986",
        "INTRACRANIAL_HEMORRHAGE": "RID4701",
        "CONSOLIDATION": "RID5226",
        "FRACTURE": "RID4784"
    }

    @classmethod
    def lookup_rid(cls, term: str) -> Optional[str]:
        clean = term.upper().replace(" ", "_")
        return cls.ANATOMY_MAP.get(clean) or cls.FINDING_MAP.get(clean)
