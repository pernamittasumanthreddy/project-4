from decimal import Decimal
from django.db import models
from apps.common.models import TenantScopedModel
from apps.billing.models import Invoice

class InsurancePayer(TenantScopedModel):
    """
    Insurance Company, TPA, or Government Health Scheme.
    """
    PAYER_TYPE_CHOICES = [
        ('PRIVATE_INSURER', 'Private Health Insurer'),
        ('GOVERNMENT_SCHEME', 'Government Health Scheme (PM-JAY / CGHS / ECHS)'),
        ('CORPORATE_TPA', 'Third Party Administrator (TPA)'),
    ]

    code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    payer_type = models.CharField(max_length=30, choices=PAYER_TYPE_CHOICES, default='PRIVATE_INSURER')
    tpa_contact_email = models.EmailField(blank=True, default='')
    tpa_contact_phone = models.CharField(max_length=30, blank=True, default='')
    settlement_tat_days = models.PositiveIntegerField(default=14, help_text="Typical Turnaround Time in Days")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} [{self.code}]"


class InsurancePolicy(TenantScopedModel):
    """
    Patient insurance policy coverage record.
    """
    patient_id = models.CharField(max_length=64, db_index=True)
    patient_name = models.CharField(max_length=255)
    payer = models.ForeignKey(InsurancePayer, on_delete=models.CASCADE, related_name='policies')
    policy_number = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100, blank=True, default='')
    sum_insured = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('500000.00'))
    copay_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('10.00'))
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Policy {self.policy_number} ({self.payer.name}) - {self.patient_name}"


class InsuranceClaim(TenantScopedModel):
    """
    Hospital Insurance Claim for cashless or reimbursement billing.
    """
    STATUS_CHOICES = [
        ('PREPARING', 'Claim Documentation Preparing'),
        ('PRE_AUTH_PENDING', 'Pre-Authorization Pending'),
        ('SUBMITTED', 'Submitted to Payer / TPA'),
        ('PENDING_REVIEW', 'Under Payer Review'),
        ('APPROVED', 'Fully Approved by Insurer'),
        ('PARTIALLY_APPROVED', 'Partially Approved (Deductions Applied)'),
        ('REJECTED', 'Claim Rejected / Denied'),
        ('RESUBMITTED', 'Resubmitted with Deficiencies Resolved'),
        ('SETTLED', 'Claim Settled & Disbursed'),
    ]

    claim_number = models.CharField(max_length=100, unique=True, db_index=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='insurance_claims')
    payer = models.ForeignKey(InsurancePayer, on_delete=models.PROTECT, related_name='claims')
    policy = models.ForeignKey(InsurancePolicy, on_delete=models.SET_NULL, null=True, blank=True)
    
    pre_auth_number = models.CharField(max_length=100, blank=True, default='')
    claim_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    patient_copay_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    deductible_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    settled_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='SUBMITTED', db_index=True)
    submission_date = models.DateField(auto_now_add=True)
    adjudication_date = models.DateField(null=True, blank=True)
    denial_reason = models.TextField(blank=True, default='')
    settlement_reference = models.CharField(max_length=100, blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.claim_number} - {self.payer.name} (Claim ₹{self.claim_amount}) [{self.status}]"


class DenialLog(TenantScopedModel):
    """
    Denial Workbench tracking log for rejected/partially approved claims.
    """
    DENIAL_CODE_CHOICES = [
        ('DOCS_MISSING', 'Missing Clinical Discharge Summary / Documents'),
        ('NON_COVERED', 'Non-payable / Exclusion Item Billed'),
        ('PRE_AUTH_EXCEEDED', 'Billed Amount Exceeded Pre-Auth Limit'),
        ('DIAGNOSIS_MISMATCH', 'Clinical Diagnosis Mismatch with Policy Coverage'),
        ('TARIFF_DISPUTE', 'Line Item Rate Exceeded Agreed TPA Tariff Schedule'),
        ('POLICY_EXPIRED', 'Coverage Period Expired at Date of Admission'),
    ]

    claim = models.ForeignKey(InsuranceClaim, on_delete=models.CASCADE, related_name='denial_logs')
    denial_code = models.CharField(max_length=40, choices=DENIAL_CODE_CHOICES, default='DOCS_MISSING')
    denial_reason = models.TextField()
    corrective_action_taken = models.TextField(blank=True, default='')
    resubmitted_claim_reference = models.CharField(max_length=100, blank=True, default='')
    logged_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"DenialLog for {self.claim.claim_number} [{self.denial_code}]"
