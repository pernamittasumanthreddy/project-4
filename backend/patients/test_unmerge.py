import pytest
from core.models import Tenant
from patients.models import Patient, PatientMergeAudit
from patients.unmerge_service import PatientMergeRollbackService


@pytest.mark.django_db
def test_patient_merge_rollback_service():
    tenant = Tenant.objects.create(name="Community Health", slug="community-health")

    survivor = Patient.objects.create(
        tenant=tenant,
        mrn="MRN-SURVIVOR-01",
        first_name="Robert",
        last_name="Johnson",
        phone="+919811122233"
    )

    subsumed = Patient.objects.create(
        tenant=tenant,
        mrn="MRN-SUBSUMED-02",
        first_name="Bob",
        last_name="Johnson",
        phone="+919811122233",
        is_merged=True,
        merged_into=survivor,
        status="MERGED"
    )

    audit = PatientMergeAudit.objects.create(
        tenant=tenant,
        surviving_patient=survivor,
        subsumed_patient=subsumed,
        subsumed_mrn_snapshot=subsumed.mrn,
        merged_by_user_id="admin_1",
        merged_by_user_email="admin@test.com",
        reason="Initial duplicate merge test",
        snapshot_data={"first_name": "Bob", "last_name": "Johnson"}
    )

    res = PatientMergeRollbackService.rollback_merge(
        audit_id=str(audit.id),
        tenant=tenant,
        rollback_user_id="auditor_user",
        rollback_reason="False positive duplicate merge resolution"
    )

    assert res["status"] == "SUCCESS"
    subsumed.refresh_from_db()
    assert subsumed.is_merged is False
    assert subsumed.merged_into is None
    assert subsumed.status == "ACTIVE"
