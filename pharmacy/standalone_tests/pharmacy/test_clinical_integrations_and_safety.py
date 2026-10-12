"""Tests for Clinical Interoperability, FHIR, HL7, and Safety Engines — Member 5"""

import pytest
from decimal import Decimal
from datetime import date, timedelta

from core.models import Tenant, Hospital, Branch
from accounts.models import User, UserRole
from clinical.models import Patient, Prescription, PrescriptionItem, PrescriptionStatus
from pharmacy.models.catalogue import Medicine, DosageForm, DrugClassification
from pharmacy.models.inventory import MedicineBatch, BatchStatus, StorageLocation
from pharmacy.models.dispensing import DispenseRecord, DispensedItem
from pharmacy.models.cold_chain import TemperatureLog
from pharmacy.services.clinical_safety import ClinicalSafetyEngine, InteractionSeverity
from pharmacy.integrations.fhir_adapters import FHIRAdapter
from pharmacy.integrations.hl7_engine import HL7MessageEngine
from pharmacy.services.barcode_verification import BarcodeVerificationService


@pytest.fixture
def clinical_setup():
    tenant = Tenant.objects.create(name="St. Interop Hospital", subdomain="interop-hosp")
    hospital = Hospital.objects.create(tenant=tenant, name="Interop Center")
    branch = Branch.objects.create(hospital=hospital, name="Main Interop", code="MINT")

    doctor = User.objects.create_user(
        username="dr_interop", password="Password123!", role=UserRole.DOCTOR, tenant=tenant, branch=branch
    )
    pharmacist = User.objects.create_user(
        username="rph_interop", password="Password123!", role=UserRole.PHARMACIST, tenant=tenant, branch=branch
    )

    patient = Patient.objects.create(
        tenant=tenant,
        mrn="MRN-INT-001",
        full_name="Jane Doe",
        gender="FEMALE",
        date_of_birth=date(1985, 5, 20),
        contact_number="555-0199"
    )


    med_warfarin = Medicine.objects.create(
        tenant=tenant,
        code="MED-WARF-5",
        brand_name="Coumadin",
        generic_name="Warfarin Sodium",
        strength="5 mg",
        dosage_form=DosageForm.TABLET,
        classification=DrugClassification.CARDIOVASCULAR,
        barcode_sku="0100312345678901"
    )

    med_aspirin = Medicine.objects.create(
        tenant=tenant,
        code="MED-ASP-81",
        brand_name="Bayer Aspirin",
        generic_name="Aspirin (Acetylsalicylic Acid)",
        strength="81 mg",
        dosage_form=DosageForm.TABLET,
        classification=DrugClassification.ANALGESIC
    )

    med_amox = Medicine.objects.create(
        tenant=tenant,
        code="MED-AMX-500",
        brand_name="Amoxil",
        generic_name="Amoxicillin Trihydrate",
        strength="500 mg",
        dosage_form=DosageForm.CAPSULE,
        classification=DrugClassification.ANTIBIOTIC
    )

    batch_warfarin = MedicineBatch.objects.create(
        tenant=tenant,
        branch=branch,
        medicine=med_warfarin,
        batch_number="LOT-WARF-01",
        expiry_date=date.today() + timedelta(days=300),
        purchase_cost=Decimal("5.00"),
        selling_price=Decimal("10.00"),
        received_quantity=Decimal("100.00"),
        available_quantity=Decimal("100.00"),
        status=BatchStatus.ACTIVE
    )

    return tenant, branch, doctor, pharmacist, patient, med_warfarin, med_aspirin, med_amox, batch_warfarin


@pytest.mark.django_db
class TestClinicalSafetyAndInteroperability:
    """Verifies DDI safety rules, allergy cross-reactivity, FHIR R4 JSON, and HL7 v2 messages."""

    def test_drug_drug_interaction_detection(self, clinical_setup):
        """Verifies that life-threatening DDI pairs (Warfarin + Aspirin) are detected with CONTRAINDICATED severity."""
        _, _, _, _, _, med_warfarin, med_aspirin, med_amox, _ = clinical_setup

        alerts = ClinicalSafetyEngine.check_drug_interactions([med_warfarin, med_aspirin])
        assert len(alerts) >= 1
        alert = alerts[0]
        assert alert.severity == InteractionSeverity.CONTRAINDICATED
        assert "hemorrhage" in alert.clinical_effect.lower() or "bleeding" in alert.clinical_effect.lower()

        # Non-interacting pair
        safe_alerts = ClinicalSafetyEngine.check_drug_interactions([med_warfarin, med_amox])
        assert len(safe_alerts) == 0

    def test_patient_allergy_cross_reactivity(self, clinical_setup):
        """Verifies that penicillin allergy triggers critical cross-reactivity warnings on amoxicillin."""
        _, _, _, _, _, _, _, med_amox, _ = clinical_setup

        allergies = ["Penicillins", "Peanuts"]
        alerts = ClinicalSafetyEngine.check_patient_allergies(med_amox, allergies)
        assert len(alerts) >= 1
        assert alerts[0].allergen_class == "PENICILLINS"
        assert alerts[0].severity == "CRITICAL"

    def test_fhir_medication_request_conversion(self, clinical_setup):
        """Verifies that an HMS Prescription converts to valid FHIR R4 MedicationRequest JSON."""
        tenant, branch, doctor, _, patient, med_warfarin, _, _, _ = clinical_setup

        rx = Prescription.objects.create(
            tenant=tenant,
            patient=patient,
            prescriber=doctor,
            prescription_number="RX-FHIR-1001",
            status=PrescriptionStatus.PENDING
        )
        PrescriptionItem.objects.create(
            prescription=rx,
            medicine_code=med_warfarin.code,
            medicine_name="Coumadin 5mg",
            quantity_prescribed=Decimal("30.00"),
            dosage="5 mg",
            frequency="Once daily in the evening",
            duration_days=30,
            instructions="Target INR 2.0-3.0"
        )

        fhir_data = FHIRAdapter.to_fhir_medication_request(rx)
        assert fhir_data["resourceType"] == "MedicationRequest"
        assert fhir_data["status"] == "active"
        assert fhir_data["subject"]["display"] == "Jane Doe"
        assert fhir_data["dosageInstruction"][0]["additionalInstruction"][0]["text"] == "Target INR 2.0-3.0"

    def test_hl7_rds_and_dft_message_generation(self, clinical_setup):
        """Verifies HL7 v2 RDS^O13 dispense and DFT^P03 billing message compliance."""
        tenant, branch, doctor, pharmacist, patient, med_warfarin, _, _, batch = clinical_setup

        rx = Prescription.objects.create(
            tenant=tenant, patient=patient, prescriber=doctor, prescription_number="RX-HL7-2002"
        )
        rx_item = PrescriptionItem.objects.create(
            prescription=rx,
            medicine_code=med_warfarin.code,
            medicine_name="Coumadin 5mg",
            dosage="5 mg",
            quantity_prescribed=Decimal("10.00")
        )


        dispense = DispenseRecord.objects.create(
            tenant=tenant,
            prescription=rx,
            pharmacist=pharmacist,
            dispense_number="DSP-HL7-8888",
            total_amount=Decimal("100.00")
        )
        DispensedItem.objects.create(
            dispense_record=dispense,
            prescription_item=rx_item,
            medicine=med_warfarin,
            batch=batch,
            quantity_dispensed=Decimal("10.00"),
            unit_price=Decimal("10.00")
        )


        # 1. HL7 Dispense Message (RDS)
        rds_msg = HL7MessageEngine.create_rds_dispense_message(dispense)
        assert rds_msg.startswith("MSH|^~\\&|HMS_PHARMACY")
        assert "RDS^O13" in rds_msg
        assert "PID|1||MRN-INT-001" in rds_msg
        assert "Coumadin" in rds_msg
        assert "LOT-WARF-01" in rds_msg

        # 2. HL7 Billing Message (DFT)
        dft_msg = HL7MessageEngine.create_dft_financial_transaction_message(dispense)
        assert "DFT^P03" in dft_msg
        assert "FT1|1" in dft_msg
        assert "PHARM_CHARGE" in dft_msg

        # 3. Parse HL7 Message
        parsed = HL7MessageEngine.parse_hl7_message(rds_msg)
        assert "MSH" in parsed["segments"]
        assert "PID" in parsed["segments"]
        assert "RXD" in parsed["segments"]
        assert parsed["message_type"] == "RDS^O13"

    def test_gs1_datamatrix_barcode_verification(self, clinical_setup):
        """Verifies GS1 DataMatrix scanning, AI parsing, and expiration safety stops."""
        tenant, branch, _, _, _, med_warfarin, _, _, batch = clinical_setup

        # Valid GS1 scan string: (01)00312345678901(17)271231(10)LOT-WARF-01
        valid_scan = "(01)00312345678901(17)271231(10)LOT-WARF-01"
        res = BarcodeVerificationService.verify_scan_against_inventory(tenant, valid_scan, branch)
        assert res.is_verified is True
        assert res.status == "VERIFIED_ELIGIBLE"
        assert res.medicine.code == "MED-WARF-5"

        # Expired batch safety stop
        batch.expiry_date = date.today() - timedelta(days=1)
        batch.save()
        res_expired = BarcodeVerificationService.verify_scan_against_inventory(tenant, valid_scan, branch)
        assert res_expired.is_verified is False
        assert res_expired.status == "EXPIRED_BLOCK"

    def test_cold_chain_thermal_excursion_logging(self, clinical_setup):
        """Verifies that out-of-spec temperatures are automatically flagged as thermal excursions."""
        tenant, branch, _, _, _, _, _, _, _ = clinical_setup
        cold_loc = StorageLocation.objects.create(
            tenant=tenant, branch=branch, code="FRIDGE-TST-01", name="Test Vaccine Fridge", is_cold_storage=True
        )

        # Normal temperature (4.5°C) -> is_excursion False
        log_normal = TemperatureLog.objects.create(
            tenant=tenant, storage_location=cold_loc, recorded_temperature_celsius=Decimal("4.50")
        )
        assert log_normal.is_excursion is False

        # Excursion temperature (12.5°C) -> is_excursion True
        log_warm = TemperatureLog.objects.create(
            tenant=tenant, storage_location=cold_loc, recorded_temperature_celsius=Decimal("12.50")
        )
        assert log_warm.is_excursion is True
