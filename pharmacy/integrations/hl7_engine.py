"""HMS HL7 v2.x Standards Engine — Member 5
Implements bi-directional HL7 message generation and parsing for hospital automated dispensing
cabinets (e.g., Pyxis, Omnicell), pharmacy information systems (PIS), and hospital billing engines:
- MSH (Message Header)
- PID (Patient Identification)
- PV1 (Patient Visit)
- ORC (Common Order)
- RXO (Pharmacy/Treatment Order)
- RXD (Pharmacy/Treatment Dispense)
- FT1 (Financial Transaction)
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from decimal import Decimal
import uuid

from pharmacy.models.dispensing import DispenseRecord
from clinical.models import Prescription, PrescriptionItem



class HL7MessageEngine:
    """Encodes and decodes standard pipe-and-hat delimited HL7 v2.5.1 messages."""

    FIELD_SEP = "|"
    COMP_SEP = "^"
    REP_SEP = "~"
    ESC_CHAR = "\\"
    SUBCOMP_SEP = "&"

    @classmethod
    def generate_msh_segment(cls, message_type: str, trigger_event: str, message_control_id: Optional[str] = None) -> str:
        """Generates standard MSH (Message Header) segment."""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        msg_id = message_control_id or f"MSG{timestamp[-6:]}{str(uuid.uuid4())[:4]}"
        return f"MSH|^~\\&|HMS_PHARMACY|HOSPITAL_MAIN|AUTOMATED_DISPENSE|PIS|{timestamp}||{message_type}^{trigger_event}|{msg_id}|P|2.5.1"

    @classmethod
    def generate_pid_segment(cls, patient) -> str:
        """Generates standard PID (Patient Identification) segment."""
        mrn = patient.mrn or "UNKNOWN_MRN"
        name_parts = patient.full_name.split()
        last_name = name_parts[-1] if name_parts else "PATIENT"
        first_name = " ".join(name_parts[:-1]) if len(name_parts) > 1 else ""
        dob = patient.date_of_birth.strftime("%Y%m%d") if patient.date_of_birth else ""
        gender = patient.gender[:1].upper() if patient.gender else "U"

        return f"PID|1||{mrn}^^^HOSPITAL^MR||{last_name}^{first_name}||{dob}|{gender}|||{getattr(patient, 'contact_number', '') or ''}"


    @classmethod
    def generate_pv1_segment(cls, patient, visit_number: str = "VN10001") -> str:
        """Generates standard PV1 (Patient Visit) segment."""
        return f"PV1|1|I|PHARM_INPATIENT^BED01^ROOM101|||||||||||||||{visit_number}"

    @classmethod
    def create_rds_dispense_message(cls, dispense: DispenseRecord) -> str:
        """Constructs an HL7 RDS^O13 (Pharmacy/Treatment Dispense) message.
        Sent to automated dispensing machines (Pyxis/Omnicell) upon pharmacist verification.
        """
        segments = []
        segments.append(cls.generate_msh_segment("RDS", "O13", f"DISP{dispense.id}"))
        segments.append(cls.generate_pid_segment(dispense.prescription.patient))
        segments.append(cls.generate_pv1_segment(dispense.prescription.patient))

        # Order Common Segment (ORC)
        rx_time = dispense.prescription.created_at.strftime("%Y%m%d%H%M%S")
        segments.append(f"ORC|RE|{dispense.prescription.prescription_number}^HMS|{dispense.dispense_number}^PHARM||||||{rx_time}|{dispense.pharmacist.username}^RPH")

        # Dispense Segment (RXD) for each allocated item
        for item in dispense.items.all():
            batch = item.batch
            medicine = batch.medicine
            dispense_time = dispense.created_at.strftime("%Y%m%d%H%M%S")
            expiry = batch.expiry_date.strftime("%Y%m%d")

            price = getattr(item, 'unit_price', Decimal('0.00'))
            rxd = (
                f"RXD|1|{medicine.code}^{medicine.brand_name}^HMS|{dispense_time}|"
                f"{item.quantity_dispensed}|{medicine.dispensing_unit}|"
                f"{price}|{batch.batch_number}|{expiry}||"
                f"{batch.storage_location.name if batch.storage_location else 'MAIN_STORE'}"
            )
            segments.append(rxd)

        return "\r".join(segments)

    @classmethod
    def create_dft_financial_transaction_message(cls, dispense: DispenseRecord) -> str:
        """Constructs an HL7 DFT^P03 (Detailed Financial Transaction) message.
        Sent to Member 6's hospital billing engine to invoice medication charges.
        """
        segments = []
        segments.append(cls.generate_msh_segment("DFT", "P03", f"BILL{dispense.id}"))
        segments.append(cls.generate_pid_segment(dispense.prescription.patient))
        segments.append(cls.generate_pv1_segment(dispense.prescription.patient))

        timestamp = dispense.created_at.strftime("%Y%m%d%H%M%S")

        # Financial Transaction Segments (FT1)
        for idx, item in enumerate(dispense.items.all(), start=1):
            batch = item.batch
            medicine = batch.medicine
            price = getattr(item, 'unit_price', Decimal('0.00'))
            line_total = item.quantity_dispensed * price

            ft1 = (
                f"FT1|{idx}||{timestamp}|{timestamp}|CG|PHARM_CHARGE^Pharmacy Medication Charge|"
                f"{medicine.code}^{medicine.brand_name}|{item.quantity_dispensed}|{price}|"
                f"{line_total}|PHARM_DEPT||||||||{dispense.pharmacist.username}"
            )
            segments.append(ft1)


        return "\r".join(segments)

    @classmethod
    def parse_hl7_message(cls, raw_message: str) -> Dict[str, Any]:
        """Parses a pipe-delimited HL7 message into structured segment dictionaries."""
        parsed = {"segments": [], "message_type": "", "control_id": "", "fields": {}}
        lines = [line.strip() for line in raw_message.replace("\r\n", "\r").replace("\n", "\r").split("\r") if line.strip()]

        for line in lines:
            parts = line.split(cls.FIELD_SEP)
            seg_name = parts[0]
            parsed["segments"].append(seg_name)

            if seg_name == "MSH":
                if len(parts) > 8:
                    parsed["message_type"] = parts[8]
                if len(parts) > 9:
                    parsed["control_id"] = parts[9]
            parsed["fields"][seg_name] = parts

        return parsed
