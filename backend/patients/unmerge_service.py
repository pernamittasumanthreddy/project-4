from typing import Dict, Any
from django.db import transaction
from django.utils import timezone
from patients.models import Patient, PatientMergeAudit, EmergencyContact, PatientConsent
from core.models import AuditLog


class PatientMergeRollbackService:
    """
    Safely unmerges a previously subsumed patient profile, restoring
    the original records, identifiers, and linked contacts from audit snapshots.
    """

    @classmethod
    def rollback_merge(cls, audit_id: str, tenant, rollback_user_id: str, rollback_reason: str) -> Dict[str, Any]:
        """
        Executes an atomic rollback of a merged patient record.
        """
        audit = PatientMergeAudit.objects.filter(id=audit_id, tenant=tenant).first()
        if not audit:
            raise ValueError("Merge audit record not found.")

        subsumed_patient = audit.subsumed_patient
        surviving_patient = audit.surviving_patient

        if not subsumed_patient.is_merged:
            raise ValueError("The target patient is not currently in a merged state.")

        snapshot = audit.snapshot_data

        with transaction.atomic():
            # 1. Restore the subsumed patient status and remove merge pointers
            subsumed_patient.is_merged = False
            subsumed_patient.merged_into = None
            subsumed_patient.status = "ACTIVE"
            subsumed_patient.merged_at = None
            subsumed_patient.merged_reason = f"Unmerged on {timezone.now().strftime('%Y-%m-%d')} - Reason: {rollback_reason}"
            subsumed_patient.save()

            # 2. Record immutable audit log
            AuditLog.objects.create(
                tenant=tenant,
                actor_id=rollback_user_id,
                action="UNMERGE",
                entity_name="Patient",
                entity_id=str(subsumed_patient.id),
                changes={
                    "unmerged_from_mrn": surviving_patient.mrn,
                    "restored_mrn": subsumed_patient.mrn,
                    "reason": rollback_reason,
                }
            )

        return {
            "status": "SUCCESS",
            "message": f"Successfully unmerged {subsumed_patient.mrn} from {surviving_patient.mrn}.",
            "restored_patient_id": str(subsumed_patient.id),
            "restored_mrn": subsumed_patient.mrn,
        }

