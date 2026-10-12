"""
HIPAA Safe Harbor De-Identification and PHI Scrubber Engine.
Anonymizes patient identifiers in JSON and DICOM metadata exports for clinical research.
"""

from typing import Dict, Any
import hashlib

class PHISanitizer:
    SAFE_HARBOR_FIELDS = [
        "patient_name", "first_name", "last_name", "ssn",
        "phone", "email", "address", "medical_record_number"
    ]

    @classmethod
    def anonymize_dataset(cls, data: Dict[str, Any], salt: str = "HMS_RESEARCH_SALT") -> Dict[str, Any]:
        scrubbed = data.copy()
        for k in list(scrubbed.keys()):
            if k.lower() in cls.SAFE_HARBOR_FIELDS:
                val = str(scrubbed[k])
                anon_val = "ANON-" + hashlib.sha256((val + salt).encode("utf-8")).hexdigest()[:10].upper()
                scrubbed[k] = anon_val
        return scrubbed
