"""
Automated Integration Contract Tests for Teammates (Members 1, 2, 3, 5, 6).
"""
import pytest
from contracts.billing_bus import BillingEventBus
from contracts.patient_matcher import PatientIdentityMatcher
from contracts.encounter_linker import EncounterContextLinker, ClinicalEncounterContext
from contracts.drug_lab_interference import DrugLabInterferenceMatrix
from contracts.tenant_audit import TenantIsolationAuditor

def test_member_6_billing_event_bus():
    event = BillingEventBus.emit_charge(
        tenant_id="TENANT-001", patient_id="PT-001", source_module="LIS",
        order_id="ORD-101", item_code="CBC", item_name="Complete Blood Count",
        amount_cents=4500
    )
    assert event.event_id.startswith("EVT-")
    assert event.amount_cents == 4500
    assert event.status == "PENDING"

def test_member_2_patient_identity_matcher():
    registry = {
        "PT-1": {"mrn": "MRN-100", "full_name": "JOHN DOE", "dob": "1980-01-01"},
        "PT-2": {"mrn": "MRN-200", "full_name": "JANE SMITH", "dob": "1992-05-10"}
    }
    match = PatientIdentityMatcher.match_patient("MRN-200", "Jane Smith", "1992-05-10", registry)
    assert match == "PT-2"

def test_member_3_encounter_context_linker():
    ctx = ClinicalEncounterContext("ENC-999", "ICU", "Bed-04", "DOC-42", "Septic shock")
    order = {"order_id": "ORD-500", "test": "Blood Culture"}
    linked = EncounterContextLinker.link_order_to_encounter(order, ctx)
    assert linked["encounter_id"] == "ENC-999"
    assert linked["encounter_class"] == "ICU"
    assert linked["bed_location"] == "Bed-04"

def test_member_5_drug_lab_interference():
    alerts = DrugLabInterferenceMatrix.check_active_medications("TSH", ["Biotin", "Aspirin"])
    assert len(alerts) > 0
    assert alerts[0]["effect"] == "FALSE_LOW"

def test_member_1_tenant_isolation_auditor():
    data = [{"id": 1, "tenant_id": "TENANT-A"}, {"id": 2, "tenant_id": "TENANT-A"}]
    assert TenantIsolationAuditor.audit_records_isolation("TENANT-A", data) is True
    assert TenantIsolationAuditor.audit_records_isolation("TENANT-B", data) is False
