import uuid
from django.db import models
from django.utils import timezone
from core.models import TenantAwareModel, HospitalBranch, Department
from patients.models import Patient


class Ward(TenantAwareModel):
    """
    Hospital Ward or Inpatient Unit (e.g. General Male Ward, ICU, Pediatric, Maternity).
    """
    WARD_TYPES = [
        ("GENERAL", "General Ward"),
        ("ICU", "Intensive Care Unit (ICU)"),
        ("NICU", "Neonatal ICU"),
        ("PEDIATRIC", "Pediatric Ward"),
        ("MATERNITY", "Maternity / Labour Ward"),
        ("EMERGENCY", "Emergency Observation"),
        ("ISOLATION", "Isolation Ward"),
        ("PRIVATE", "Private Rooms Suite"),
    ]

    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name="wards")
    name = models.CharField(max_length=150)
    ward_type = models.CharField(max_length=30, choices=WARD_TYPES, default="GENERAL")
    floor = models.CharField(max_length=50, blank=True, default="")
    total_beds = models.PositiveIntegerField(default=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hms_wards"
        unique_together = ("tenant", "branch", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_ward_type_display()}) - {self.branch.name}"


class Room(TenantAwareModel):
    """
    Room within a ward or private corridor.
    """
    ROOM_TYPES = [
        ("STANDARD", "Standard Shared Room"),
        ("DELUXE", "Single Deluxe Room"),
        ("SUITE", "Executive VIP Suite"),
        ("ICU_POD", "ICU Pod"),
    ]

    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name="rooms")
    room_number = models.CharField(max_length=50)
    room_type = models.CharField(max_length=30, choices=ROOM_TYPES, default="STANDARD")
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hms_rooms"
        unique_together = ("ward", "room_number")
        ordering = ["room_number"]

    def __str__(self):
        return f"Room {self.room_number} [{self.ward.name}]"


class Bed(TenantAwareModel):
    """
    Individual bed with occupancy status state machine.
    """
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("OCCUPIED", "Occupied"),
        ("RESERVED", "Reserved for Incoming Patient"),
        ("CLEANING", "Under Cleaning / Sanitization"),
        ("MAINTENANCE", "Under Maintenance / Inoperable"),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="beds")
    bed_number = models.CharField(max_length=50)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="AVAILABLE", db_index=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "hms_beds"
        unique_together = ("room", "bed_number")
        ordering = ["bed_number"]

    def __str__(self):
        return f"Bed {self.bed_number} ({self.room.room_number}) - [{self.status}]"


class Admission(TenantAwareModel):
    """
    Inpatient Admission Lifecycle (IPD).
    Coordinates bed stay, admitting clinician, transfer history, and billing clearance.
    """
    STATUS_CHOICES = [
        ("ADMITTED", "Currently Admitted"),
        ("DISCHARGE_REQUESTED", "Discharge Requested (Awaiting Clearances)"),
        ("BILLING_CLEARED", "Billing Cleared"),
        ("DISCHARGED", "Discharged"),
        ("TRANSFERRED_OUT", "Transferred to External Facility"),
        ("DECEASED", "Deceased"),
    ]

    admission_number = models.CharField(
        max_length=50,
        db_index=True,
        help_text="Unique IPD identifier, e.g. IPD-2026-0001"
    )
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name="admissions")
    branch = models.ForeignKey(HospitalBranch, on_delete=models.CASCADE, related_name="admissions")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="admissions")
    admitting_doctor_id = models.CharField(max_length=100, db_index=True)
    admitting_doctor_name = models.CharField(max_length=200)

    bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name="admissions")
    admission_date = models.DateTimeField(default=timezone.now, db_index=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="ADMITTED", db_index=True)

    admission_diagnosis = models.TextField(help_text="Provisional diagnosis upon hospital admission")
    discharge_diagnosis = models.TextField(blank=True, default="")
    discharge_summary = models.TextField(blank=True, default="")

    billing_cleared = models.BooleanField(default=False)
    billing_cleared_at = models.DateTimeField(null=True, blank=True)
    billing_cleared_by = models.CharField(max_length=100, blank=True, default="")

    class Meta:
        db_table = "hms_admissions"
        unique_together = ("tenant", "admission_number")
        ordering = ["-admission_date"]

    def __str__(self):
        return f"{self.admission_number} - {self.patient.full_name} ({self.status})"


class BedTransferLog(TenantAwareModel):
    """
    Tracks clinical bed-to-bed and ward-to-ward transfers during patient admission.
    """
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name="transfers")
    from_bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name="transfers_from")
    to_bed = models.ForeignKey(Bed, on_delete=models.PROTECT, related_name="transfers_to")
    transfer_time = models.DateTimeField(default=timezone.now)
    transferred_by_user_id = models.CharField(max_length=100)
    transferred_by_user_name = models.CharField(max_length=200)
    reason = models.TextField(help_text="Clinical justification for bed or ward transfer")

    class Meta:
        db_table = "hms_bed_transfers"
        ordering = ["-transfer_time"]

    def __str__(self):
        return f"Transfer #{self.admission.admission_number}: {self.from_bed.bed_number} -> {self.to_bed.bed_number}"
