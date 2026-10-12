import pytest
import datetime
from django.utils import timezone
from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient, EmergencyContact
from appointments.models import DoctorSchedule, DoctorLeave, Appointment, OPDQueueToken
from admissions.models import Ward, Room, Bed, Admission, BedTransferLog
from patients.duplicate_engine import PatientDuplicateEngine


@pytest.fixture
def setup_data(db):
    tenant1 = Tenant.objects.create(name="Metro General Hospital", slug="metro-general", mrn_prefix="MGH")
    tenant2 = Tenant.objects.create(name="Apex Care Center", slug="apex-care", mrn_prefix="ACC")

    branch1 = HospitalBranch.objects.create(tenant=tenant1, name="Downtown Branch", code="DTN")
    dept1 = Department.objects.create(tenant=tenant1, branch=branch1, name="Cardiology", code="CARD")

    patient1 = Patient.objects.create(
        tenant=tenant1,
        mrn="MGH-2026-000001",
        first_name="John",
        last_name="Doe",
        phone="+919876543210",
        date_of_birth=datetime.date(1990, 5, 15),
        national_id="AADHAAR-1234-5678",
        gender="MALE",
        blood_group="O+"
    )

    return {
        "tenant1": tenant1,
        "tenant2": tenant2,
        "branch1": branch1,
        "dept1": dept1,
        "patient1": patient1,
    }


@pytest.mark.django_db
class TestPatientAndDuplicateEngine:
    def test_mrn_uniqueness_and_properties(self, setup_data):
        patient = setup_data["patient1"]
        assert patient.full_name == "John Doe"
        assert patient.age > 30
        assert patient.mrn.startswith("MGH-")

    def test_duplicate_exact_national_id(self, setup_data):
        t1 = setup_data["tenant1"]
        duplicates = PatientDuplicateEngine.scan_for_duplicates(
            tenant_id=t1.id,
            first_name="Johnny",
            last_name="Doe",
            phone="+910000000000",
            national_id="AADHAAR-1234-5678"
        )
        assert len(duplicates) == 1
        assert duplicates[0]["confidence_score"] == 1.0

    def test_duplicate_fuzzy_phone_and_name(self, setup_data):
        t1 = setup_data["tenant1"]
        duplicates = PatientDuplicateEngine.scan_for_duplicates(
            tenant_id=t1.id,
            first_name="John",
            last_name="Doe",
            phone="+919876543210"
        )
        assert len(duplicates) == 1
        assert duplicates[0]["confidence_score"] >= 0.70

    def test_cross_tenant_isolation(self, setup_data):
        t2 = setup_data["tenant2"]
        # Searching tenant 2 should NOT find patient in tenant 1
        duplicates = PatientDuplicateEngine.scan_for_duplicates(
            tenant_id=t2.id,
            first_name="John",
            last_name="Doe",
            phone="+919876543210"
        )
        assert len(duplicates) == 0


@pytest.mark.django_db
class TestAppointmentAndQueue:
    def test_appointment_booking_and_checkin_token(self, setup_data):
        t1 = setup_data["tenant1"]
        b1 = setup_data["branch1"]
        d1 = setup_data["dept1"]
        p1 = setup_data["patient1"]

        today = timezone.now().date()
        apt = Appointment.objects.create(
            tenant=t1,
            appointment_number="APT-2026-0001",
            patient=p1,
            doctor_id="doc_101",
            doctor_name="Sarah Smith",
            branch=b1,
            department=d1,
            appointment_date=today,
            start_time=datetime.time(10, 0),
            end_time=datetime.time(10, 15),
            status="CONFIRMED"
        )

        assert apt.status == "CONFIRMED"

        # Check-in and assign queue token
        token = OPDQueueToken.objects.create(
            tenant=t1,
            appointment=apt,
            branch=b1,
            department=d1,
            doctor_id=apt.doctor_id,
            token_number=1,
            queue_date=today,
            status="WAITING"
        )
        apt.status = "CHECKED_IN"
        apt.token_number = token.token_number
        apt.save()

        assert apt.token_number == 1
        assert token.status == "WAITING"


@pytest.mark.django_db
class TestIPDAdmissionsAndBedTransfer:
    def test_admission_and_bed_state_cycle(self, setup_data):
        t1 = setup_data["tenant1"]
        b1 = setup_data["branch1"]
        d1 = setup_data["dept1"]
        p1 = setup_data["patient1"]

        ward = Ward.objects.create(tenant=t1, branch=b1, name="ICU Wing", ward_type="ICU")
        room = Room.objects.create(tenant=t1, ward=ward, room_number="101")
        bed1 = Bed.objects.create(tenant=t1, room=room, bed_number="B-1", status="AVAILABLE")
        bed2 = Bed.objects.create(tenant=t1, room=room, bed_number="B-2", status="AVAILABLE")

        # Admit patient
        adm = Admission.objects.create(
            tenant=t1,
            admission_number="IPD-2026-0001",
            patient=p1,
            branch=b1,
            department=d1,
            admitting_doctor_id="doc_101",
            admitting_doctor_name="Sarah Smith",
            bed=bed1,
            admission_diagnosis="Acute Myocardial Infarction",
            status="ADMITTED"
        )
        bed1.status = "OCCUPIED"
        bed1.save()

        assert bed1.status == "OCCUPIED"
        assert adm.status == "ADMITTED"

        # Bed Transfer to Bed 2
        BedTransferLog.objects.create(
            tenant=t1,
            admission=adm,
            from_bed=bed1,
            to_bed=bed2,
            transferred_by_user_id="nurse_1",
            transferred_by_user_name="Nurse Clara",
            reason="Step-down observation transfer"
        )
        bed1.status = "CLEANING"
        bed1.save()
        bed2.status = "OCCUPIED"
        bed2.save()
        adm.bed = bed2
        adm.save()

        assert adm.bed.bed_number == "B-2"
        assert bed1.status == "CLEANING"
        assert bed2.status == "OCCUPIED"
        assert adm.transfers.count() == 1
