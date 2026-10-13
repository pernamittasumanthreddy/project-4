import pytest
from datetime import date, timedelta
from django.utils import timezone
from contracts.models import Tenant, HospitalBranch, UserProfile, UserRole, PatientContract, ClinicalEncounterContract, BillingEventContract
from lis.models import (
    LabCategory, LabTest, LabTestPanel, LabOrder, LabOrderItem,
    Specimen, SpecimenEvent, LabResult, CriticalResultAlert, LabReport,
    SpecimenType, LabOrderStatus, SpecimenStatus, ResultStatus, OrderPriority
)
from ris.models import (
    ImagingModality, ImagingProcedure, ImagingOrder, ImagingOrderItem,
    ImagingStudy, RadiologyReport, ModalityType, ImagingOrderStatus, RadiologyReportStatus
)
from lis.pdf_generator import generate_lab_report_pdf
from ris.pdf_generator import generate_radiology_report_pdf
from ris.dicom_service import generate_synthetic_dicom_file, render_dicom_to_png_bytes

@pytest.mark.django_db
class TestMember4LISModule:
    """Automated verification for Member 4 Laboratory Information System"""

    def test_test_catalogue_and_reference_range_evaluation(self):
        tenant = Tenant.objects.create(name='Test Hospital', code='test-hosp')
        category = LabCategory.objects.create(name='Biochemistry', code='BIO')
        test = LabTest.objects.create(
            tenant=tenant, category=category, test_code='GLUC-01', name='Fasting Glucose',
            specimen_type=SpecimenType.SERUM, unit='mg/dL',
            ref_min=70.0, ref_max=99.0, critical_low=45.0, critical_high=400.0, price=20.0
        )

        assert test.evaluate_numeric_flag(85.0) == 'NORMAL'
        assert test.evaluate_numeric_flag(60.0) == 'LOW'
        assert test.evaluate_numeric_flag(140.0) == 'HIGH'
        assert test.evaluate_numeric_flag(35.0) == 'CRITICAL_LOW'
        assert test.evaluate_numeric_flag(450.0) == 'CRITICAL_HIGH'

    def test_order_creation_and_duplicate_prevention(self, client):
        tenant = Tenant.objects.create(name='Hospital Alpha', code='hosp-alpha')
        branch = HospitalBranch.objects.create(tenant=tenant, branch_code='ALPHA-1', name='Alpha Branch', city='City', state='State')
        patient = PatientContract.objects.create(
            tenant=tenant, branch=branch, uhid='UHID-101', first_name='John', last_name='Doe',
            dob=date(1990, 1, 1), gender='M', phone='12345'
        )
        cat = LabCategory.objects.create(name='Hematology', code='HEM')
        test = LabTest.objects.create(
            tenant=tenant, category=cat, test_code='CBC-HGB', name='Hemoglobin',
            specimen_type=SpecimenType.WHOLE_BLOOD, price=15.0
        )

        # 1. First order creation
        resp1 = client.post('/api/laboratory/orders/', {
            'patient_id': str(patient.id),
            'test_ids': [str(test.id)],
            'ordering_clinician': 'Dr. Smith',
            'priority': 'ROUTINE',
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')

        assert resp1.status_code == 201
        order_data = resp1.json()
        assert order_data['status'] == 'SAMPLE_PENDING'
        assert len(order_data['items']) == 1
        assert len(order_data['specimens']) == 1

        # 2. Duplicate order check within 15 minutes should return 409 Conflict
        resp2 = client.post('/api/laboratory/orders/', {
            'patient_id': str(patient.id),
            'test_ids': [str(test.id)],
            'ordering_clinician': 'Dr. Smith',
            'priority': 'ROUTINE',
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')

        assert resp2.status_code == 409
        assert 'Duplicate Order Detected' in resp2.json()['error']

    def test_specimen_collection_and_rejection_workflow(self, client):
        tenant = Tenant.objects.create(name='Hospital Alpha', code='hosp-alpha')
        branch = HospitalBranch.objects.create(tenant=tenant, branch_code='ALPHA-1', name='Alpha Branch', city='City', state='State')
        patient = PatientContract.objects.create(
            tenant=tenant, branch=branch, uhid='UHID-102', first_name='Alice', last_name='Smith',
            dob=date(1985, 3, 10), gender='F', phone='98765'
        )
        cat = LabCategory.objects.create(name='Biochemistry', code='BIO')
        test = LabTest.objects.create(tenant=tenant, category=cat, test_code='ALT', name='ALT', price=20.0)

        order = LabOrder.objects.create(tenant=tenant, branch=branch, patient=patient, ordering_clinician='Dr. Smith')
        specimen = Specimen.objects.create(
            order=order, specimen_type=SpecimenType.SERUM, container_type='Gold SST Tube', status=SpecimenStatus.PENDING
        )

        # Collection
        res_col = client.post(f'/api/laboratory/specimens/{specimen.id}/collect_sample/', {
            'collected_by': 'Phlebotomist Vance'
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_col.status_code == 200
        specimen.refresh_from_db()
        assert specimen.status == SpecimenStatus.COLLECTED

        # Rejection
        res_rej = client.post(f'/api/laboratory/specimens/{specimen.id}/reject_sample/', {
            'reason': 'Hemolyzed Specimen',
            'notes': 'Specimen clotted and hemolyzed.',
            'actor_name': 'QA Officer'
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_rej.status_code == 200
        specimen.refresh_from_db()
        assert specimen.status == SpecimenStatus.REJECTED
        assert specimen.recollection_needed is True

    def test_critical_result_alert_and_acknowledgement(self, client):
        tenant = Tenant.objects.create(name='Hospital Alpha', code='hosp-alpha')
        branch = HospitalBranch.objects.create(tenant=tenant, branch_code='ALPHA-1', name='Alpha Branch', city='City', state='State')
        patient = PatientContract.objects.create(
            tenant=tenant, branch=branch, uhid='UHID-103', first_name='Bob', last_name='Miller',
            dob=date(1970, 6, 20), gender='M', phone='55512'
        )
        cat = LabCategory.objects.create(name='Cardiac', code='CAR')
        test = LabTest.objects.create(
            tenant=tenant, category=cat, test_code='TROP-TEST', name='Troponin I',
            unit='ng/L', ref_min=0.0, ref_max=14.0, critical_high=50.0, price=45.0
        )
        order = LabOrder.objects.create(tenant=tenant, branch=branch, patient=patient, ordering_clinician='Dr. House')
        item = LabOrderItem.objects.create(order=order, test=test)
        result = LabResult.objects.create(order_item=item, test=test, unit='ng/L')

        # Enter critical result: 92.5 ng/L (> critical_high 50.0)
        res_ent = client.post(f'/api/laboratory/results/{result.id}/enter_result/', {
            'numeric_value': 92.5,
            'entered_by': 'Tech Kim'
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_ent.status_code == 200
        assert res_ent.json()['flag'] == 'CRITICAL_HIGH'
        assert res_ent.json()['is_critical'] is True

        # Verify Critical Alert record auto-created
        alert = CriticalResultAlert.objects.filter(result=result).first()
        assert alert is not None
        assert alert.alert_status == 'TRIGGERED'

        # Clinician acknowledges
        res_ack = client.post(f'/api/laboratory/critical-alerts/{alert.id}/acknowledge/', {
            'acknowledged_by': 'Dr. House',
            'call_log_notes': 'Verified critical elevation; patient scheduled for cath lab.'
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_ack.status_code == 200
        alert.refresh_from_db()
        assert alert.alert_status == 'ACKNOWLEDGED'

    def test_result_approval_report_generation_and_billing_contract(self, client):
        tenant = Tenant.objects.create(name='Hospital Alpha', code='hosp-alpha')
        branch = HospitalBranch.objects.create(tenant=tenant, branch_code='ALPHA-1', name='Alpha Branch', city='City', state='State')
        patient = PatientContract.objects.create(
            tenant=tenant, branch=branch, uhid='UHID-104', first_name='Carol', last_name='Danvers',
            dob=date(1988, 9, 15), gender='F', phone='44400'
        )
        cat = LabCategory.objects.create(name='Biochemistry', code='BIO')
        test = LabTest.objects.create(tenant=tenant, category=cat, test_code='GLUC', name='Glucose', ref_min=70, ref_max=99, price=25.0)
        order = LabOrder.objects.create(tenant=tenant, branch=branch, patient=patient, ordering_clinician='Dr. Smith')
        item = LabOrderItem.objects.create(order=order, test=test)
        result = LabResult.objects.create(order_item=item, test=test, numeric_value=85.0, status=ResultStatus.ENTERED)

        # Consultant Pathologist approves result
        res_app = client.post(f'/api/laboratory/results/{result.id}/approve_result/', {
            'approved_by': 'Dr. Sarah Al-Mansoor, MD'
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_app.status_code == 200
        order.refresh_from_db()
        assert order.status == LabOrderStatus.APPROVED

        # Verify LabReport was created
        report = LabReport.objects.filter(order=order).first()
        assert report is not None
        assert report.approved_by == 'Dr. Sarah Al-Mansoor, MD'

        # Verify PDF can be generated without error
        pdf_bytes = generate_lab_report_pdf(report)
        assert pdf_bytes.startswith(b'%PDF')
        assert len(pdf_bytes) > 1000

        # Verify Member 6 Billing Event Contract was emitted
        billing_event = BillingEventContract.objects.filter(module='LIS', order_id=order.order_number).first()
        assert billing_event is not None
        assert billing_event.service_code == 'GLUC'
        assert float(billing_event.amount) == 25.0

@pytest.mark.django_db
class TestMember4RISModule:
    """Automated verification for Member 4 Radiology Information System & DICOMweb"""

    def test_imaging_order_scan_completion_and_dicom_generation(self, client):
        tenant = Tenant.objects.create(name='Hospital Alpha', code='hosp-alpha')
        branch = HospitalBranch.objects.create(tenant=tenant, branch_code='ALPHA-1', name='Alpha Branch', city='City', state='State')
        patient = PatientContract.objects.create(
            tenant=tenant, branch=branch, uhid='UHID-201', first_name='David', last_name='Tennant',
            dob=date(1971, 4, 18), gender='M', phone='77711'
        )
        modality = ImagingModality.objects.create(name='CT Scanner 01', modality_type='CT')
        proc = ImagingProcedure.objects.create(
            tenant=tenant, modality=modality, procedure_code='RAD-CT-CHEST', name='CT Thorax', body_part='Chest', price=350.0
        )

        # Create Order
        res_ord = client.post('/api/radiology/orders/', {
            'patient_id': str(patient.id),
            'procedure_ids': [str(proc.id)],
            'ordering_clinician': 'Dr. McCoy',
            'priority': 'URGENT',
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_ord.status_code == 201
        order_id = res_ord.json()['id']

        # Technologist completes scan
        res_comp = client.post(f'/api/radiology/orders/{order_id}/complete_scan/', {
            'technologist': 'Marcus Vance, RT(R)'
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_comp.status_code == 200

        # Check ImagingStudy and synthetic DICOM generation
        study = ImagingStudy.objects.filter(patient=patient).first()
        assert study is not None
        assert study.modality_type == 'CT'
        assert study.dicom_file_path != ''

        # Verify rendered frame endpoint returns valid PNG
        res_render = client.get(
            f'/api/dicomweb/studies/{study.study_instance_uid}/series/{study.study_instance_uid}.1/instances/{study.study_instance_uid}.1.1/rendered',
            HTTP_X_TENANT_CODE='hosp-alpha'
        )
        assert res_render.status_code == 200
        assert res_render['Content-Type'] == 'image/png'
        assert res_render.content.startswith(b'\x89PNG')

    def test_radiology_reporting_signoff_and_pdf(self, client):
        tenant = Tenant.objects.create(name='Hospital Alpha', code='hosp-alpha')
        branch = HospitalBranch.objects.create(tenant=tenant, branch_code='ALPHA-1', name='Alpha Branch', city='City', state='State')
        patient = PatientContract.objects.create(
            tenant=tenant, branch=branch, uhid='UHID-202', first_name='Emma', last_name='Watson',
            dob=date(1990, 4, 15), gender='F', phone='99922'
        )
        modality = ImagingModality.objects.create(name='X-Ray Suite', modality_type='DX')
        proc = ImagingProcedure.objects.create(
            tenant=tenant, modality=modality, procedure_code='RAD-XR-CHEST', name='Chest X-Ray', body_part='Chest', price=90.0
        )
        order = ImagingOrder.objects.create(tenant=tenant, branch=branch, patient=patient, ordering_clinician='Dr. House')
        item = ImagingOrderItem.objects.create(order=order, procedure=proc)
        study = ImagingStudy.objects.create(
            order_item=item, patient=patient, accession_number='RAD-XR-99', modality_type='DX', study_description='Chest X-Ray'
        )
        report = RadiologyReport.objects.create(
            study=study, reporting_radiologist='Dr. Sterling, MD',
            findings='Lungs are clear bilaterally.', impression='Normal chest radiograph.'
        )

        # Consultant approves report
        res_app = client.post(f'/api/radiology/reports/{report.id}/approve_report/', {
            'approved_by': 'Dr. Sterling, MD',
            'findings': 'Lungs are clear bilaterally without consolidation.',
            'impression': 'No acute pulmonary disease.'
        }, content_type='application/json', HTTP_X_TENANT_CODE='hosp-alpha')
        assert res_app.status_code == 200
        report.refresh_from_db()
        assert report.status == RadiologyReportStatus.APPROVED

        # Verify PDF generation
        pdf_bytes = generate_radiology_report_pdf(report)
        assert pdf_bytes.startswith(b'%PDF')
        assert len(pdf_bytes) > 1000

@pytest.mark.django_db
class TestMultiTenantIsolation:
    """Rigorous Tenant Isolation tests: Hospital A cannot see or download Hospital B's data"""

    def test_tenant_data_isolation(self, client):
        tenant_a = Tenant.objects.create(name='Hospital A', code='hosp-a')
        tenant_b = Tenant.objects.create(name='Hospital B', code='hosp-b')

        branch_a = HospitalBranch.objects.create(tenant=tenant_a, branch_code='A-1', name='Branch A', city='City', state='State')
        branch_b = HospitalBranch.objects.create(tenant=tenant_b, branch_code='B-1', name='Branch B', city='City', state='State')

        patient_a = PatientContract.objects.create(
            tenant=tenant_a, branch=branch_a, uhid='UHID-A1', first_name='Patient', last_name='Alpha',
            dob=date(1990, 1, 1), gender='M', phone='111'
        )
        patient_b = PatientContract.objects.create(
            tenant=tenant_b, branch=branch_b, uhid='UHID-B1', first_name='Patient', last_name='Beta',
            dob=date(1992, 2, 2), gender='F', phone='222'
        )

        order_a = LabOrder.objects.create(tenant=tenant_a, branch=branch_a, patient=patient_a, ordering_clinician='Dr. A')
        order_b = LabOrder.objects.create(tenant=tenant_b, branch=branch_b, patient=patient_b, ordering_clinician='Dr. B')

        # Query orders as Tenant A
        res_a = client.get('/api/laboratory/orders/', HTTP_X_TENANT_CODE='hosp-a')
        assert res_a.status_code == 200
        data_a = res_a.json()
        ids_in_a = [o['id'] for o in (data_a.get('results') or data_a)]
        assert str(order_a.id) in ids_in_a
        assert str(order_b.id) not in ids_in_a  # Hospital B's order MUST NOT appear!

        # Query orders as Tenant B
        res_b = client.get('/api/laboratory/orders/', HTTP_X_TENANT_CODE='hosp-b')
        assert res_b.status_code == 200
        data_b = res_b.json()
        ids_in_b = [o['id'] for o in (data_b.get('results') or data_b)]
        assert str(order_b.id) in ids_in_b
        assert str(order_a.id) not in ids_in_b  # Hospital A's order MUST NOT appear!
