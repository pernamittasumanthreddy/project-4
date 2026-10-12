"""
Cryptographic Electronic Signature and Seal Verification for Pathologist Reports.
Produces HMAC-SHA256 digital seals ensuring report immutability under 21 CFR Part 11.
"""

import hmac
import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, Any

class PathologistDigitalSigner:
    SYSTEM_SECRET = b"HMS-MEMBER4-PATHOLOGY-SIGNATURE-KEY-SECURE-2026"

    @classmethod
    def generate_report_seal(cls, tenant_id: str, report_id: str, accession_number: str,
                             pathologist_license: str, report_text_hash: str) -> Dict[str, Any]:
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = f"{tenant_id}:{report_id}:{accession_number}:{pathologist_license}:{report_text_hash}:{timestamp}"
        signature = hmac.new(cls.SYSTEM_SECRET, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return {
            "signature_algorithm": "HMAC-SHA256",
            "signed_at": timestamp,
            "pathologist_license": pathologist_license,
            "report_hash": report_text_hash,
            "digital_seal": signature
        }

    @classmethod
    def verify_seal(cls, tenant_id: str, report_id: str, accession_number: str,
                    pathologist_license: str, report_text_hash: str,
                    timestamp: str, seal_to_verify: str) -> bool:
        payload = f"{tenant_id}:{report_id}:{accession_number}:{pathologist_license}:{report_text_hash}:{timestamp}"
        expected = hmac.new(cls.SYSTEM_SECRET, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected, seal_to_verify)
