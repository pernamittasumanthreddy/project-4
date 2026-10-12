from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.tenants.models import Tenant, Branch
from apps.billing.models import BillingEntity, Invoice
from apps.insurance.models import InsurancePayer, InsurancePolicy, InsuranceClaim, DenialLog

class InsuranceModuleTests(TestCase):
    def setUp(self):
        self.tenant = Tenant.objects.create(name="Care Hospitals", slug="care-hyd", default_currency="INR")
        self.branch = Branch.objects.create(tenant=self.tenant, name="Care Banjara", code="CARE-BAN", city="Hyderabad", state_code="36")
        self.billing_entity = BillingEntity.objects.create(
            tenant=self.tenant, branch=self.branch, name="Care Legal",
            legal_name="Care Hospital Ltd", gstin="36CARE0000A1Z1", pan="CARE1234", state_code="36"
        )
        self.invoice = Invoice.objects.create(
            tenant=self.tenant, billing_entity=self.billing_entity,
            invoice_number="INV-CARE-01", patient_id="PAT-301", patient_name="Meera Sen",
            patient_state_code="36", status="ISSUED", issue_date=timezone.now().date(), due_date=timezone.now().date(),
            total_net=Decimal('75000.00'), balance_due=Decimal('75000.00')
        )
        self.payer = InsurancePayer.objects.create(
            tenant=self.tenant, code="STAR-CARE", name="Star Health Insurance", payer_type="PRIVATE_INSURER"
        )
        self.policy = InsurancePolicy.objects.create(
            tenant=self.tenant, patient_id="PAT-301", patient_name="Meera Sen",
            payer=self.payer, policy_number="POL-CARE-99", sum_insured=Decimal('500000.00'),
            copay_percentage=Decimal('10.00'), valid_from=timezone.now().date(), valid_to=timezone.now().date()
        )

    def test_claim_lifecycle_and_denial_workbench_resubmission(self):
        """Verifies claim submission, denial logging in workbench, and subsequent resubmission."""
        claim = InsuranceClaim.objects.create(
            tenant=self.tenant,
            claim_number="CLM-CARE-001",
            invoice=self.invoice,
            payer=self.payer,
            policy=self.policy,
            pre_auth_number="PA-HYD-9901",
            claim_amount=Decimal('75000.00'),
            status="SUBMITTED"
        )
        self.assertEqual(claim.status, "SUBMITTED")

        # Insurer Rejection
        claim.status = "REJECTED"
        claim.denial_reason = "Pre-authorization limit exceeded by ₹15,000"
        claim.save()

        denial_log = DenialLog.objects.create(
            tenant=self.tenant,
            claim=claim,
            denial_code="PRE_AUTH_EXCEEDED",
            denial_reason=claim.denial_reason,
            resolved=False
        )
        self.assertFalse(denial_log.resolved)
        self.assertEqual(claim.denial_logs.count(), 1)

        # Denial Workbench Resubmission with enhanced documentation
        claim.status = "RESUBMITTED"
        claim.save()
        denial_log.resolved = True
        denial_log.corrective_action_taken = "Supplemental enhancement approval letter attached."
        denial_log.resubmitted_claim_reference = "CLM-CARE-001-R1"
        denial_log.save()

        self.assertEqual(claim.status, "RESUBMITTED")
        self.assertTrue(denial_log.resolved)
        self.assertEqual(denial_log.resubmitted_claim_reference, "CLM-CARE-001-R1")
