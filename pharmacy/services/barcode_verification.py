"""HMS GS1 DataMatrix & Barcode Medication Verification Engine — Member 5
Implements GS1 Application Identifier (AI) standard parsing and clinical bedside/dispense verification:
- AI (01): GTIN (Global Trade Item Number)
- AI (17): Expiration Date (YYMMDD)
- AI (10): Batch / Lot Number
- AI (21): Serial Number
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime, date
from dataclasses import dataclass

from pharmacy.models.inventory import MedicineBatch
from pharmacy.models.catalogue import Medicine


@dataclass
class GS1ParsedData:
    raw_barcode: str
    gtin: Optional[str] = None
    batch_number: Optional[str] = None
    expiry_date: Optional[date] = None
    serial_number: Optional[str] = None
    is_valid_gs1: bool = False


@dataclass
class VerificationResult:
    is_verified: bool
    status: str
    message: str
    batch: Optional[MedicineBatch] = None
    medicine: Optional[Medicine] = None


class BarcodeVerificationService:
    """Parses 2D GS1 DataMatrix barcodes and validates safety constraints against persisted stock."""

    # Matches GS1 Application Identifiers like (01)00300450444558(17)261231(10)LOT12345
    AI_PAREN_REGEX = re.compile(r'\((\d{2})\)([^\(\)]+)')

    @classmethod
    def parse_gs1_barcode(cls, raw_code: str) -> GS1ParsedData:
        """Extracts GTIN, batch number, expiry date, and serial number from raw GS1 scan."""
        cleaned = raw_code.strip()
        data = GS1ParsedData(raw_barcode=cleaned)

        # 1. Try formatted parentheses format: (01)...(17)...(10)...
        matches = cls.AI_PAREN_REGEX.findall(cleaned)
        if matches:
            for ai, val in matches:
                if ai == "01":
                    data.gtin = val
                elif ai == "10":
                    data.batch_number = val
                elif ai == "17":
                    data.expiry_date = cls._parse_yymmdd(val)
                elif ai == "21":
                    data.serial_number = val
            data.is_valid_gs1 = bool(data.gtin or data.batch_number)
            return data

        # 2. Try raw GS1 element string e.g. 01003004504445581726123110LOT12345
        if cleaned.startswith("01") and len(cleaned) >= 16:
            data.gtin = cleaned[2:16]
            remainder = cleaned[16:]
            if remainder.startswith("17") and len(remainder) >= 8:
                data.expiry_date = cls._parse_yymmdd(remainder[2:8])
                remainder = remainder[8:]
            if remainder.startswith("10"):
                data.batch_number = remainder[2:]
            data.is_valid_gs1 = True
            return data

        # 3. Fallback: treat as plain internal SKU or batch string
        data.batch_number = cleaned
        data.is_valid_gs1 = False
        return data

    @classmethod
    def _parse_yymmdd(cls, yymmdd_str: str) -> Optional[date]:
        """Parses YYMMDD string into date object."""
        try:
            if len(yymmdd_str) == 6:
                year = 2000 + int(yymmdd_str[:2])
                month = int(yymmdd_str[2:4])
                day = int(yymmdd_str[4:6])
                # GS1 convention: day 00 means last day of month
                if day == 0:
                    day = 28
                return date(year, month, day)
        except Exception:
            pass
        return None

    @classmethod
    def verify_scan_against_inventory(cls, tenant, raw_barcode: str, branch=None) -> VerificationResult:
        """Verifies scanned package against tenant's active database inventory."""
        parsed = cls.parse_gs1_barcode(raw_barcode)

        # Query batch by extracted lot or raw code
        batch_query = MedicineBatch.objects.filter(tenant=tenant)
        if branch:
            batch_query = batch_query.filter(branch=branch)

        batch = None
        if parsed.batch_number:
            batch = batch_query.filter(batch_number=parsed.batch_number).first()

        if not batch and parsed.gtin:
            batch = batch_query.filter(medicine__barcode_sku=parsed.gtin).first()

        if not batch:
            # Fallback to medicine lookup
            med = Medicine.objects.filter(tenant=tenant, barcode_sku=raw_barcode).first()
            if med:
                return VerificationResult(
                    is_verified=True,
                    status="MEDICINE_MATCHED_NO_BATCH",
                    message=f"Product matched {med.brand_name}, but specific lot not verified.",
                    medicine=med
                )
            return VerificationResult(
                is_verified=False,
                status="NOT_FOUND",
                message="Scanned package lot or barcode does not match any inventory record in this facility."
            )

        # Verify lot safety
        today = date.today()
        if batch.expiry_date <= today:
            return VerificationResult(
                is_verified=False,
                status="EXPIRED_BLOCK",
                message=f"CRITICAL SAFETY STOP: Batch {batch.batch_number} expired on {batch.expiry_date}. Dispensing strictly prohibited.",
                batch=batch,
                medicine=batch.medicine
            )

        if batch.status in ['QUARANTINED', 'RECALLED']:
            return VerificationResult(
                is_verified=False,
                status="RECALL_BLOCK",
                message=f"CRITICAL SAFETY STOP: Batch {batch.batch_number} is under {batch.status} hold.",
                batch=batch,
                medicine=batch.medicine
            )

        if batch.available_quantity <= 0:
            return VerificationResult(
                is_verified=False,
                status="DEPLETED_BLOCK",
                message=f"Batch {batch.batch_number} has zero recorded available units.",
                batch=batch,
                medicine=batch.medicine
            )

        return VerificationResult(
            is_verified=True,
            status="VERIFIED_ELIGIBLE",
            message=f"Verification successful: {batch.medicine.brand_name} (Lot: {batch.batch_number}, Expiry: {batch.expiry_date}). Safe for dispensing.",
            batch=batch,
            medicine=batch.medicine
        )
