"""
CLSI H26-A2 Pre-Analytical Specimen Rejection and Recollection Engine.
Tracks pre-analytical errors (hemolysis, lipemia, clotting, improper anticoagulant)
and triggers automated recollection tasks.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional, Dict

@dataclass
class RejectionReasonCode:
    code: str
    description: str
    category: str  # SPECIMEN_QUALITY, VOLUME, CONTAINER, IDENTIFICATION

REJECTION_DICTIONARY: Dict[str, RejectionReasonCode] = {
    "HEM": RejectionReasonCode("HEM", "Grossly Hemolyzed Sample", "SPECIMEN_QUALITY"),
    "LIP": RejectionReasonCode("LIP", "Severely Lipemic Sample", "SPECIMEN_QUALITY"),
    "ICT": RejectionReasonCode("ICT", "Icteric Sample Interferences", "SPECIMEN_QUALITY"),
    "CLT": RejectionReasonCode("CLT", "Clotted Whole Blood Tube", "SPECIMEN_QUALITY"),
    "QNS": RejectionReasonCode("QNS", "Quantity Not Sufficient (QNS)", "VOLUME"),
    "TINC": RejectionReasonCode("TINC", "Incorrect Tube Type / Anticoagulant", "CONTAINER"),
    "MISL": RejectionReasonCode("MISL", "Mislabeled / Missing Patient Identifier", "IDENTIFICATION"),
    "TEMP": RejectionReasonCode("TEMP", "Improper Transport Temperature", "SPECIMEN_QUALITY"),
}

@dataclass
class SpecimenRejectionRecord:
    rejection_id: str
    tenant_id: str
    accession_number: str
    patient_id: str
    test_code: str
    reason_code: str
    reason_description: str
    rejected_by_technologist_id: str
    timestamp: datetime
    recollection_requested: bool = True
    phlebotomy_notified: bool = True

class SpecimenRejectionHandler:
    @staticmethod
    def reject_specimen(rejection_id: str, tenant_id: str, accession_number: str,
                        patient_id: str, test_code: str, reason_code: str,
                        technologist_id: str) -> SpecimenRejectionRecord:
        info = REJECTION_DICTIONARY.get(reason_code.upper())
        desc = info.description if info else "Other Pre-analytical Specimen Defect"
        return SpecimenRejectionRecord(
            rejection_id=rejection_id,
            tenant_id=tenant_id,
            accession_number=accession_number,
            patient_id=patient_id,
            test_code=test_code,
            reason_code=reason_code.upper(),
            reason_description=desc,
            rejected_by_technologist_id=technologist_id,
            timestamp=datetime.now(timezone.utc),
            recollection_requested=True,
            phlebotomy_notified=True
        )
