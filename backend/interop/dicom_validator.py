"""
DICOM PS3.3 Information Object Definition (IOD) SOP Class Validator.
Validates presence of mandatory Type 1 patient, study, series, and image attributes.
"""

from typing import Dict, Any, List

class DICOMIODValidator:
    MANDATORY_TAGS = [
        "PatientName", "PatientID", "StudyInstanceUID",
        "SeriesInstanceUID", "SOPInstanceUID", "Modality"
    ]

    @classmethod
    def validate_dataset(cls, tags: Dict[str, Any]) -> List[str]:
        missing = []
        for tag in cls.MANDATORY_TAGS:
            if tag not in tags or not tags[tag]:
                missing.append(tag)
        return missing
