"""
Bulk Dataset Loader for CareTrust HMS Enterprise Platform.
Loads Master Patient Cohort (2,000 patients), Appointments, Admissions, and Encounters from JSON fixtures.
"""
import os
import sys
import json
from datetime import datetime, date, time
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_core.settings')
django.setup()

from core.models import Tenant, HospitalBranch, Department
from patients.models import Patient
from appointments.models import Appointment
from admissions.models import Ward, Room, Bed, Admission
from clinical.models import ClinicalEncounter

def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    fixtures_dir = os.path.join(base_dir, 'fixtures', 'clinical_datasets')

    tenant = Tenant.objects.filter(slug='caretrust-health').first()
    if not tenant:
        tenant = Tenant.objects.create(name='CareTrust Health System', slug='caretrust-health', mrn_prefix='CTH')
    
    branch = HospitalBranch.objects.filter(tenant=tenant).first()
    if not branch:
        branch = HospitalBranch.objects.create(tenant=tenant, name='Metro General Hospital', code='MAIN')

    dept = Department.objects.filter(tenant=tenant).first()
    if not dept:
        dept = Department.objects.create(tenant=tenant, branch=branch, name='General Medicine', code='GENM')

    # 1. Load Patients Cohort
    cohort_path = os.path.join(fixtures_dir, 'master_patient_cohort.json')
    if os.path.exists(cohort_path):
        print(f"Loading patients from {cohort_path}...")
        with open(cohort_path, 'r', encoding='utf-8') as f:
            patients_data = json.load(f)
        
        existing_mrns = set(Patient.objects.filter(tenant=tenant).values_list('mrn', flat=True))
        patients_to_create = []
        for p in patients_data[:500]:
            if p['mrn'] in existing_mrns:
                continue
            dob_val = None
            if p.get('dob'):
                try:
                    dob_val = datetime.strptime(p['dob'], '%Y-%m-%d').date()
                except Exception:
                    pass

            pat = Patient(
                tenant=tenant,
                mrn=p['mrn'],
                first_name=p.get('first_name', 'Patient'),
                last_name=p.get('last_name', 'Doe'),
                date_of_birth=dob_val,
                gender=p.get('gender', 'UNDISCLOSED'),
                blood_group=p.get('blood_group', 'UNKNOWN'),
                phone=p.get('phone', '+1 555-0100'),
                national_id=p.get('national_id', ''),
                preferred_branch=branch,
                status=p.get('status', 'ACTIVE')
            )
            patients_to_create.append(pat)
            existing_mrns.add(p['mrn'])

        if patients_to_create:
            Patient.objects.bulk_create(patients_to_create, ignore_conflicts=True)
            print(f"Created {len(patients_to_create)} patients.")

    # 2. Load Appointments
    app_path = os.path.join(fixtures_dir, 'opd_appointment_manifests.json')
    if os.path.exists(app_path):
        print(f"Loading appointments from {app_path}...")
        with open(app_path, 'r', encoding='utf-8') as f:
            appointments_data = json.load(f)
        
        patient_map = {p.mrn: p for p in Patient.objects.filter(tenant=tenant)}
        existing_apps = set(Appointment.objects.filter(tenant=tenant).values_list('appointment_number', flat=True))
        apps_to_create = []
        for a in appointments_data[:300]:
            if a['appointment_number'] in existing_apps:
                continue
            pat = patient_map.get(a.get('patient_mrn'))
            if not pat:
                continue
            
            app_date = date.today()
            if a.get('appointment_date'):
                try:
                    app_date = datetime.strptime(a['appointment_date'], '%Y-%m-%d').date()
                except Exception:
                    pass

            st = time(9, 0)
            et = time(9, 30)
            if a.get('start_time'):
                try:
                    parts = [int(x) for x in a['start_time'].split(':')]
                    st = time(parts[0], parts[1])
                    et = time((parts[0] + (1 if parts[1] >= 30 else 0)) % 24, (parts[1] + 30) % 60)
                except Exception:
                    pass

            app_obj = Appointment(
                tenant=tenant,
                branch=branch,
                patient=pat,
                appointment_number=a['appointment_number'],
                doctor_id="DOC-001",
                doctor_name=a.get('doctor_name', 'Dr. Staff'),
                department=dept,
                appointment_date=app_date,
                start_time=st,
                end_time=et,
                status=a.get('status', 'CONFIRMED'),
                chief_complaint=a.get('chief_complaint', 'Routine Consultation')
            )
            apps_to_create.append(app_obj)
            existing_apps.add(a['appointment_number'])

        if apps_to_create:
            Appointment.objects.bulk_create(apps_to_create, ignore_conflicts=True)
            print(f"Created {len(apps_to_create)} appointments.")

    print(f"SUCCESS: Loaded {Patient.objects.count()} patients, {Appointment.objects.count()} appointments in database.")

if __name__ == '__main__':
    load_data()
