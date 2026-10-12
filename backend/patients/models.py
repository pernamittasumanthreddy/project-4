import uuid
from django.db import models
from django.utils import timezone
from core.models import TenantAwareModel, HospitalBranch


class Patient(TenantAwareModel):
    """
    Patient Master Record (Master Patient Index - MPI).
    Represents an individual patient profile within an isolated tenant boundary.
    """
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
        ("OTHER", "Other"),
        ("UNDISCLOSED", "Undisclosed"),
    ]

    BLOOD_GROUP_CHOICES = [
        ("A+", "A Positive"),
        ("A-", "A Negative"),
        ("B+", "B Positive"),
        ("B-", "B Negative"),
        ("AB+", "AB Positive"),
        ("AB-", "AB Negative"),
        ("O+", "O Positive"),
        ("O-", "O Negative"),
        ("UNKNOWN", "Unknown"),
    ]

    MARITAL_STATUS_CHOICES = [
        ("SINGLE", "Single"),
        ("MARRIED", "Married"),
        ("DIVORCED", "Divorced"),
        ("WIDOWED", "Widowed"),
        ("OTHER", "Other"),
    ]

    RECORD_STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("INACTIVE", "Inactive"),
        ("DECEASED", "Deceased"),
        ("MERGED", "Merged into Another Record"),
    ]

    # Core Identifiers
    mrn = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unique Medical Record Number per Tenant, e.g. MRN-2026-000001"
    )
    national_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
        help_text="National Identification (e.g. Aadhaar / SSN / National Card)"
    )
    passport_number = models.CharField(max_length=50, blank=True, default="")

    # Demographics
    first_name = models.CharField(max_length=100, db_index=True)
    middle_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, db_index=True)
    date_of_birth = models.DateField(null=True, blank=True, db_index=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default="UNDISCLOSED")
    blood_group = models.CharField(max_length=10, choices=BLOOD_GROUP_CHOICES, default="UNKNOWN")
    marital_status = models.CharField(max_length=20, choices=MARITAL_STATUS_CHOICES, default="SINGLE")

    # Contact Details
    phone = models.CharField(max_length=30, db_index=True, help_text="Primary phone with country code")
    alternate_phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="", db_index=True)

    # Address
    address_line_1 = models.CharField(max_length=255, blank=True, default="")
    address_line_2 = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    state_province = models.CharField(max_length=100, blank=True, default="")
    postal_code = models.CharField(max_length=20, blank=True, default="")
    country = models.CharField(max_length=100, default="India")

    # Primary Branch & Status
    preferred_branch = models.ForeignKey(
        HospitalBranch,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="preferred_patients"
    )
    status = models.CharField(max_length=20, choices=RECORD_STATUS_CHOICES, default="ACTIVE")

    # Duplicate resolution & Record merging
    is_merged = models.BooleanField(default=False)
    merged_into = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subsumed_patients",
        help_text="Target patient record if this profile was subsumed during a safe merge."
    )
    merged_at = models.DateTimeField(null=True, blank=True)
    merged_reason = models.TextField(blank=True, default="")

    # Medical History Summary (Extended details via Clinical Module 3)
    allergies = models.JSONField(
        default=list,
        blank=True,
        help_text="Known drug, food, or environmental allergies [{\"allergen\": \"Penicillin\", \"severity\": \"Severe\"}]"
    )
    chronic_conditions = models.JSONField(
        default=list,
        blank=True,
        help_text="List of long-term conditions [\"Type 2 Diabetes\", \"Hypertension\"]"
    )

    class Meta:
        db_table = "hms_patients"
        unique_together = ("tenant", "mrn")
        indexes = [
            models.Index(fields=["tenant", "first_name", "last_name"]),
            models.Index(fields=["tenant", "phone"]),
            models.Index(fields=["tenant", "national_id"]),
            models.Index(fields=["tenant", "date_of_birth"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.mrn} - {self.full_name}"

    @property
    def full_name(self):
        names = [self.first_name, self.middle_name, self.last_name]
        return " ".join(filter(bool, names))

    @property
    def age(self):
        if not self.date_of_birth:
            return None
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class EmergencyContact(TenantAwareModel):
    """
    Emergency contact details associated with a patient.
    """
    RELATION_CHOICES = [
        ("SPOUSE", "Spouse"),
        ("PARENT", "Parent"),
        ("CHILD", "Child"),
        ("SIBLING", "Sibling"),
        ("GUARDIAN", "Guardian"),
        ("FRIEND", "Friend"),
        ("OTHER", "Other"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="emergency_contacts")
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=30, choices=RELATION_CHOICES, default="OTHER")
    phone = models.CharField(max_length=30)
    alternate_phone = models.CharField(max_length=30, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    address = models.TextField(blank=True, default="")
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = "hms_emergency_contacts"
        ordering = ["-is_primary", "name"]

    def __str__(self):
        return f"{self.name} ({self.relationship}) for {self.patient.mrn}"


class PatientConsent(TenantAwareModel):
    """
    Formal patient consent records (General treatment, Telemedicine, Data sharing, Surgery).
    """
    CONSENT_TYPES = [
        ("GENERAL_TREATMENT", "General Inpatient/Outpatient Treatment Consent"),
        ("TELEMEDICINE", "Teleconsultation & Remote Care Consent"),
        ("DATA_SHARING", "Health Records & Diagnostic Sharing Consent"),
        ("SURGICAL_PROCEDURE", "Surgical / Invasive Procedure Consent"),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="consents")
    consent_type = models.CharField(max_length=50, choices=CONSENT_TYPES)
    title = models.CharField(max_length=255)
    content_text = models.TextField(help_text="Wording and terms acknowledged by the patient or legal guardian")
    is_granted = models.BooleanField(default=True)
    granted_at = models.DateTimeField(default=timezone.now)
    revoked_at = models.DateTimeField(null=True, blank=True)
    signer_name = models.CharField(max_length=200)
    signer_relationship = models.CharField(max_length=50, default="SELF")
    signature_ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "hms_patient_consents"
        ordering = ["-granted_at"]

    def __str__(self):
        return f"{self.consent_type} - {self.patient.mrn} (Granted: {self.is_granted})"


class PatientMergeAudit(TenantAwareModel):
    """
    Comprehensive record audit for merged patient records.
    Allows complete reconstruction and safe unmerging if required.
    """
    surviving_patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="merge_survivor_audits")
    subsumed_patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="merge_subsumed_audits")
    subsumed_mrn_snapshot = models.CharField(max_length=50)
    merged_by_user_id = models.CharField(max_length=100)
    merged_by_user_email = models.CharField(max_length=255)
    reason = models.TextField()
    snapshot_data = models.JSONField(
        default=dict,
        help_text="Complete JSON serialization of the subsumed patient profile prior to merge"
    )

    class Meta:
        db_table = "hms_patient_merge_audits"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Merged {self.subsumed_mrn_snapshot} into {self.surviving_patient.mrn} by {self.merged_by_user_email}"
