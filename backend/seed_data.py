import os
import sys
import django
from datetime import date, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hms_core.settings')
django.setup()

from contracts.models import Tenant, HospitalBranch, UserProfile, UserRole, PatientContract, ClinicalEncounterContract, EncounterType, BillingEventContract
from lis.models import (
    LabCategory, LabTest, LabTestPanel, LabOrder, LabOrderItem,
    Specimen, SpecimenEvent, LabResult, CriticalResultAlert, LabReport,
    SpecimenType, LabOrderStatus, SpecimenStatus, ResultStatus, OrderPriority
)
from ris.models import (
    ImagingModality, ImagingProcedure, ImagingOrder, ImagingOrderItem,
    ImagingStudy, RadiologyReport, ModalityType, ImagingOrderStatus, RadiologyReportStatus
)
from ris.dicom_service import generate_synthetic_dicom_file

def seed():
    print("--- [SEEDING HMS MEMBER 4 LIS & RIS DATABASE] ---")

    # 1. Tenants (Hospital A and Hospital B to test multi-tenant isolation)
    tenant_a, _ = Tenant.objects.get_or_create(
        code='metro-general',
        defaults={
            'name': 'Metro General Hospital & Trauma Center',
            'domain': 'metro.hospital-saas.com',
            'contact_email': 'contact@metrogeneral.org',
            'phone': '+1 (555) 234-5678',
            'is_active': True
        }
    )

    tenant_b, _ = Tenant.objects.get_or_create(
        code='apex-health',
        defaults={
            'name': 'Apex Healthcare Specialty Network',
            'domain': 'apex.hospital-saas.com',
            'contact_email': 'info@apexhealth.org',
            'phone': '+1 (555) 987-6543',
            'is_active': True
        }
    )

    # Branches
    branch_a1, _ = HospitalBranch.objects.get_or_create(
        tenant=tenant_a, branch_code='METRO-MAIN',
        defaults={'name': 'Main Campus Medical Center', 'city': 'Metropolis', 'state': 'NY', 'is_main_branch': True}
    )
    branch_a2, _ = HospitalBranch.objects.get_or_create(
        tenant=tenant_a, branch_code='METRO-NORTH',
        defaults={'name': 'North Wing Diagnostic Pavilion', 'city': 'Metropolis', 'state': 'NY'}
    )

    branch_b1, _ = HospitalBranch.objects.get_or_create(
        tenant=tenant_b, branch_code='APEX-CENTRAL',
        defaults={'name': 'Apex Central Hospital', 'city': 'Capital City', 'state': 'CA', 'is_main_branch': True}
    )

    # User Profiles for RBAC testing
    roles_data = [
        ('admin_metro', 'Dr. Catherine Ross', UserRole.HOSPITAL_ADMIN, tenant_a, branch_a1),
        ('labmgr_metro', 'Dr. Vikram Patel', UserRole.LAB_MANAGER, tenant_a, branch_a1),
        ('tech_metro', 'David Kim, MLS', UserRole.LAB_TECHNICIAN, tenant_a, branch_a1),
        ('path_metro', 'Dr. Sarah Al-Mansoor, MD', UserRole.PATHOLOGIST_APPROVER, tenant_a, branch_a1),
        ('radtech_metro', 'Marcus Vance, RT(R)', UserRole.RADIOLOGY_TECHNICIAN, tenant_a, branch_a1),
        ('rad_metro', 'Dr. Arthur Sterling, MD', UserRole.RADIOLOGIST, tenant_a, branch_a1),
        ('doc_metro', 'Dr. Elena Rostova, MD', UserRole.TREATING_CLINICIAN, tenant_a, branch_a1),
        ('auditor_metro', 'Franklin Moore, CPHIMS', UserRole.AUDITOR, tenant_a, branch_a1),
        # Tenant B staff
        ('admin_apex', 'Grace Hopper, MHA', UserRole.HOSPITAL_ADMIN, tenant_b, branch_b1),
        ('doc_apex', 'Dr. Gregory House, MD', UserRole.TREATING_CLINICIAN, tenant_b, branch_b1),
    ]

    for uname, fname, role, ten, br in roles_data:
        UserProfile.objects.get_or_create(
            tenant=ten, username=uname,
            defaults={'full_name': fname, 'email': f"{uname}@{ten.code}.org", 'role': role, 'branch': br}
        )

    # 2. Patients (Member 2 Contract)
    patients_data = [
        ('UHID-2026-00101', 'Eleanor', 'Pemberton', date(1968, 4, 15), 'F', 'A+', '+1 555-0101', tenant_a, branch_a1),
        ('UHID-2026-00102', 'Marcus', 'Chen', date(1982, 11, 23), 'M', 'O+', '+1 555-0102', tenant_a, branch_a1),
        ('UHID-2026-00103', 'Aaliyah', 'Farooq', date(1995, 8, 30), 'F', 'B+', '+1 555-0103', tenant_a, branch_a1),
        ('UHID-2026-00104', 'Robert', 'Jankowski', date(1954, 2, 9), 'M', 'AB-', '+1 555-0104', tenant_a, branch_a1),
        ('UHID-2026-00105', 'Chloe', 'Dubois', date(2001, 7, 19), 'F', 'O-', '+1 555-0105', tenant_a, branch_a1),
        # Patient in Tenant B (Apex)
        ('UHID-2026-00201', 'William', 'Riker', date(1975, 5, 12), 'M', 'A-', '+1 555-0201', tenant_b, branch_b1),
    ]

    patients = {}
    for uhid, fn, ln, dob, g, bg, ph, ten, br in patients_data:
        p, _ = PatientContract.objects.get_or_create(
            tenant=ten, uhid=uhid,
            defaults={'first_name': fn, 'last_name': ln, 'dob': dob, 'gender': g, 'blood_group': bg, 'phone': ph, 'branch': br}
        )
        patients[uhid] = p

    # 3. Clinical Encounters (Member 3 Contract)
    enc_1, _ = ClinicalEncounterContract.objects.get_or_create(
        tenant=tenant_a, encounter_id='ENC-METRO-901',
        defaults={
            'branch': branch_a1, 'patient': patients['UHID-2026-00101'],
            'encounter_type': EncounterType.EMERGENCY, 'attending_doctor': 'Dr. Elena Rostova, MD',
            'department': 'Emergency Medicine', 'chief_complaint': 'Acute substernal chest pain radiating to left jaw',
            'provisional_diagnosis': 'Acute Coronary Syndrome / Rule Out Myocardial Infarction'
        }
    )

    enc_2, _ = ClinicalEncounterContract.objects.get_or_create(
        tenant=tenant_a, encounter_id='ENC-METRO-902',
        defaults={
            'branch': branch_a1, 'patient': patients['UHID-2026-00102'],
            'encounter_type': EncounterType.OPD, 'attending_doctor': 'Dr. Catherine Ross',
            'department': 'Internal Medicine', 'chief_complaint': 'Persistent fatigue, polyuria, polydipsia for 3 weeks',
            'provisional_diagnosis': 'Type 2 Diabetes Mellitus evaluation'
        }
    )

    enc_3, _ = ClinicalEncounterContract.objects.get_or_create(
        tenant=tenant_a, encounter_id='ENC-METRO-903',
        defaults={
            'branch': branch_a1, 'patient': patients['UHID-2026-00104'],
            'encounter_type': EncounterType.IPD, 'attending_doctor': 'Dr. Elena Rostova, MD',
            'department': 'Pulmonology', 'chief_complaint': 'High grade fever with productive rust-colored sputum and dyspnea',
            'provisional_diagnosis': 'Community-Acquired Lobar Pneumonia'
        }
    )

    # 4. Laboratory Categories & Catalogue
    categories_spec = [
        ('HEM', 'Hematology & Hemostasis', 'Complete blood counts, coagulation, peripheral smears', 1),
        ('BIO', 'Clinical Biochemistry', 'Metabolic panels, liver/renal profiles, enzymes, electrolytes', 2),
        ('CAR', 'Cardiac Biomarkers', 'High-sensitivity Troponin, CK-MB, Natriuretic peptides', 3),
        ('SER', 'Serology & Immunology', 'Antigen/antibody detection, viral markers, autoimmune panels', 4),
        ('MIC', 'Clinical Microbiology', 'Bacterial/fungal culture, susceptibility testing, microscopy', 5),
        ('URI', 'Urinalysis & Body Fluids', 'Chemical dry-strip analysis, urine sediment microscopy', 6),
    ]

    cats = {}
    for code, name, desc, order in categories_spec:
        c, _ = LabCategory.objects.get_or_create(code=code, defaults={'name': name, 'description': desc, 'sort_order': order})
        cats[code] = c

    # Lab Tests
    tests_spec = [
        # Hematology
        ('CBC-HGB', 'Hemoglobin (Hgb)', 'HEM', '718-7', SpecimenType.WHOLE_BLOOD, 'Lavender EDTA Tube', 'g/dL', 12.0, 16.0, 7.0, 20.0, 60, 15.00),
        ('CBC-WBC', 'White Blood Cell Count (WBC)', 'HEM', '6690-2', SpecimenType.WHOLE_BLOOD, 'Lavender EDTA Tube', '10^3/uL', 4.5, 11.0, 2.0, 30.0, 60, 15.00),
        ('CBC-PLT', 'Platelet Count (PLT)', 'HEM', '777-3', SpecimenType.WHOLE_BLOOD, 'Lavender EDTA Tube', '10^3/uL', 150.0, 450.0, 40.0, 900.0, 60, 15.00),
        # Biochemistry
        ('GLUC-FAST', 'Fasting Blood Glucose', 'BIO', '1558-6', SpecimenType.SERUM, 'Gold SST Tube', 'mg/dL', 70.0, 99.0, 45.0, 400.0, 90, 18.00),
        ('HBA1C', 'Hemoglobin A1c (Glycated)', 'BIO', '4548-4', SpecimenType.WHOLE_BLOOD, 'Lavender EDTA Tube', '%', 4.0, 5.6, None, 14.0, 120, 35.00),
        ('CREAT-SR', 'Serum Creatinine', 'BIO', '2160-0', SpecimenType.SERUM, 'Gold SST Tube', 'mg/dL', 0.6, 1.2, None, 5.0, 90, 22.00),
        ('POTASS-SR', 'Serum Potassium (K+)', 'BIO', '2823-3', SpecimenType.SERUM, 'Gold SST Tube', 'mmol/L', 3.5, 5.1, 2.8, 6.2, 60, 20.00),
        ('ALT-SR', 'Alanine Aminotransferase (ALT/SGPT)', 'BIO', '1742-6', SpecimenType.SERUM, 'Gold SST Tube', 'U/L', 7.0, 56.0, None, 500.0, 120, 24.00),
        # Cardiac Markers
        ('TROP-I', 'High-Sensitivity Troponin I (hs-cTnI)', 'CAR', '10839-9', SpecimenType.PLASMA, 'Green Heparin Tube', 'ng/L', 0.0, 14.0, None, 50.0, 45, 55.00),
        # Serology
        ('CRP-HS', 'High-Sensitivity C-Reactive Protein', 'SER', '30522-7', SpecimenType.SERUM, 'Gold SST Tube', 'mg/L', 0.0, 3.0, None, 100.0, 90, 30.00),
    ]

    tests_dict = {}
    for tcode, tname, cat_c, loinc, spec_t, cont_t, unit, rmin, rmax, clow, chigh, tat, pr in tests_spec:
        t, _ = LabTest.objects.get_or_create(
            tenant=tenant_a, test_code=tcode,
            defaults={
                'name': tname, 'category': cats[cat_c], 'loinc_code': loinc,
                'specimen_type': spec_t, 'container_type': cont_t,
                'unit': unit, 'ref_min': rmin, 'ref_max': rmax,
                'critical_low': clow, 'critical_high': chigh,
                'expected_tat_minutes': tat, 'price': pr, 'is_active': True
            }
        )
        tests_dict[tcode] = t

    # Panels
    cbc_panel, _ = LabTestPanel.objects.get_or_create(
        tenant=tenant_a, panel_code='PNL-CBC-01',
        defaults={'name': 'Complete Blood Count (CBC) with Differential', 'panel_price': 40.00}
    )
    cbc_panel.tests.set([tests_dict['CBC-HGB'], tests_dict['CBC-WBC'], tests_dict['CBC-PLT']])

    # 5. Radiology Modalities & Procedure Catalogue
    mods_spec = [
        ('DX', 'Siemens Ysio Max Digital X-Ray', 'Radiology Suite 1', 'RAD_DX_01'),
        ('CT', 'GE Revolution Apex 256-Slice CT', 'CT Scanner Suite B', 'RAD_CT_01'),
        ('MR', 'Philips Ingenia 3.0T MRI', 'MRI Shielded Bay 1', 'RAD_MR_01'),
        ('US', 'GE LOGIQ E10 Ultrasound', 'US Exam Room 3', 'RAD_US_01'),
    ]

    modalities = {}
    for mtype, mname, room, ae in mods_spec:
        m, _ = ImagingModality.objects.get_or_create(
            modality_type=mtype, name=mname,
            defaults={'room_number': room, 'ae_title': ae, 'port': 11112, 'is_active': True}
        )
        modalities[mtype] = m

    procs_spec = [
        ('RAD-XR-CHEST', 'Chest Radiograph PA & Lateral (2 Views)', 'DX', '71046', 'Chest', 85.00, 60, False),
        ('RAD-XR-KNEE', 'Knee Radiograph AP & Lateral (Left)', 'DX', '73562', 'Knee', 95.00, 60, False),
        ('RAD-CT-CHEST-CON', 'CT Chest with Intravenous Contrast (Thorax)', 'CT', '71260', 'Chest', 380.00, 180, True),
        ('RAD-CT-BRAIN-NC', 'CT Head / Brain without IV Contrast', 'CT', '70450', 'Head', 290.00, 120, False),
        ('RAD-MR-BRAIN-W', 'MRI Brain with and without Contrast 3T', 'MR', '70553', 'Brain', 680.00, 240, True),
        ('RAD-US-ABD-PELV', 'Ultrasound Whole Abdomen and Pelvis', 'US', '76700', 'Abdomen', 190.00, 90, False),
    ]

    procs = {}
    for pcode, pname, mcode, cpt, bpart, pr, tat, con in procs_spec:
        p, _ = ImagingProcedure.objects.get_or_create(
            tenant=tenant_a, procedure_code=pcode,
            defaults={
                'name': pname, 'modality': modalities[mcode], 'cpt_code': cpt,
                'body_part': bpart, 'price': pr, 'expected_tat_minutes': tat,
                'requires_contrast': con, 'is_active': True
            }
        )
        procs[pcode] = p

    # 6. Seed Realistic Laboratory Orders with complete Lifecycles
    # Order 1: STAT Troponin with CRITICAL HIGH result and Alert!
    ord_1, _ = LabOrder.objects.get_or_create(
        order_number='ORD-LAB-20261012-STAT01',
        defaults={
            'tenant': tenant_a, 'branch': branch_a1, 'patient': patients['UHID-2026-00101'],
            'encounter': enc_1, 'accession_number': 'ACC-261012-TRP99',
            'ordering_clinician': 'Dr. Elena Rostova, MD', 'priority': OrderPriority.STAT,
            'status': LabOrderStatus.APPROVED, 'clinical_indications': 'Acute chest pain, ECG shows ST depressions',
            'ordered_at': timezone.now() - timedelta(minutes=75),
            'completed_at': timezone.now() - timedelta(minutes=10)
        }
    )
    item_1, _ = LabOrderItem.objects.get_or_create(
        order=ord_1, test=tests_dict['TROP-I'],
        defaults={'status': LabOrderStatus.APPROVED, 'price_at_order': 55.00}
    )
    spec_1, _ = Specimen.objects.get_or_create(
        order=ord_1, barcode_id='SPC-261012-TRP88',
        defaults={
            'specimen_type': SpecimenType.PLASMA, 'container_type': 'Green Heparin Tube',
            'status': SpecimenStatus.RECEIVED, 'collected_by': 'Phlebotomist Senior',
            'collected_at': timezone.now() - timedelta(minutes=65),
            'received_by': 'David Kim, MLS', 'received_at': timezone.now() - timedelta(minutes=50)
        }
    )
    res_1, _ = LabResult.objects.get_or_create(
        order_item=item_1,
        defaults={
            'test': tests_dict['TROP-I'], 'numeric_value': 88.4, 'unit': 'ng/L',
            'ref_range_display': '0.0 - 14.0', 'flag': 'CRITICAL_HIGH',
            'is_abnormal': True, 'is_critical': True,
            'technician_notes': 'Verified on repeat run. Delta check elevated.',
            'entered_by': 'David Kim, MLS', 'entered_at': timezone.now() - timedelta(minutes=35),
            'validated_by': 'Dr. Vikram Patel', 'validated_at': timezone.now() - timedelta(minutes=25),
            'approved_by': 'Dr. Sarah Al-Mansoor, MD', 'approved_at': timezone.now() - timedelta(minutes=10),
            'status': ResultStatus.APPROVED
        }
    )
    # Critical Alert for Troponin
    alert_1, _ = CriticalResultAlert.objects.get_or_create(
        result=res_1,
        defaults={
            'order': ord_1, 'patient': patients['UHID-2026-00101'],
            'clinician_name': 'Dr. Elena Rostova, MD',
            'alert_level': 'LIFE_THREATENING', 'alert_status': 'ACKNOWLEDGED',
            'triggered_at': timezone.now() - timedelta(minutes=30),
            'notified_at': timezone.now() - timedelta(minutes=28),
            'notified_by': 'David Kim, MLS',
            'acknowledged_at': timezone.now() - timedelta(minutes=22),
            'acknowledged_by': 'Dr. Elena Rostova, MD',
            'call_log_notes': 'Direct phone readback completed. Patient initiated on STEMI protocol.'
        }
    )
    # Approved Lab Report
    rep_1, _ = LabReport.objects.get_or_create(
        order=ord_1,
        defaults={
            'report_number': 'REP-LAB-20261012-TRP01', 'version': 1,
            'approved_by': 'Dr. Sarah Al-Mansoor, MD', 'approved_at': timezone.now() - timedelta(minutes=10)
        }
    )

    # Order 2: Routine CBC + Glucose, Sample Pending
    ord_2, _ = LabOrder.objects.get_or_create(
        order_number='ORD-LAB-20261012-ROUT02',
        defaults={
            'tenant': tenant_a, 'branch': branch_a1, 'patient': patients['UHID-2026-00102'],
            'encounter': enc_2, 'accession_number': 'ACC-261012-MET02',
            'ordering_clinician': 'Dr. Catherine Ross', 'priority': OrderPriority.ROUTINE,
            'status': LabOrderStatus.SAMPLE_PENDING, 'clinical_indications': 'Annual health checkup, HbA1c review',
            'ordered_at': timezone.now() - timedelta(minutes=40)
        }
    )
    for t_key in ['CBC-HGB', 'GLUC-FAST']:
        item, _ = LabOrderItem.objects.get_or_create(
            order=ord_2, test=tests_dict[t_key],
            defaults={'status': LabOrderStatus.SAMPLE_PENDING, 'price_at_order': tests_dict[t_key].price}
        )
        LabResult.objects.get_or_create(
            order_item=item,
            defaults={'test': tests_dict[t_key], 'unit': tests_dict[t_key].unit, 'status': ResultStatus.DRAFT}
        )
    Specimen.objects.get_or_create(
        order=ord_2, barcode_id='SPC-261012-MET02A',
        defaults={'specimen_type': SpecimenType.WHOLE_BLOOD, 'container_type': 'Lavender EDTA Tube', 'status': SpecimenStatus.PENDING}
    )
    Specimen.objects.get_or_create(
        order=ord_2, barcode_id='SPC-261012-MET02B',
        defaults={'specimen_type': SpecimenType.SERUM, 'container_type': 'Gold SST Tube', 'status': SpecimenStatus.PENDING}
    )

    # 7. Seed Realistic Radiology Orders, DICOM Studies & Reports
    # Study 1: Chest X-Ray for Pneumonia patient, DICOM Study Generated & Report Approved!
    rad_ord_1, _ = ImagingOrder.objects.get_or_create(
        order_number='ORD-RAD-20261012-XR01',
        defaults={
            'tenant': tenant_a, 'branch': branch_a1, 'patient': patients['UHID-2026-00104'],
            'encounter': enc_3, 'accession_number': 'RAD-261012-XR44',
            'ordering_clinician': 'Dr. Elena Rostova, MD', 'priority': 'URGENT',
            'status': ImagingOrderStatus.APPROVED, 'clinical_history': 'Fever, cough, rales in right mid-lung zone',
            'ordered_at': timezone.now() - timedelta(hours=3),
            'completed_at': timezone.now() - timedelta(hours=1)
        }
    )
    rad_item_1, _ = ImagingOrderItem.objects.get_or_create(
        order=rad_ord_1, procedure=procs['RAD-XR-CHEST'],
        defaults={'price_at_order': 85.00}
    )
    study_1, _ = ImagingStudy.objects.get_or_create(
        order_item=rad_item_1,
        defaults={
            'patient': patients['UHID-2026-00104'],
            'study_instance_uid': '1.2.840.10008.5.1.4.1.1.20261012.1001',
            'accession_number': 'RAD-261012-XR44',
            'modality_type': ModalityType.XRAY,
            'study_description': 'Chest Radiograph PA & Lateral (2 Views)',
            'performing_technologist': 'Marcus Vance, RT(R)',
            'series_count': 1, 'instance_count': 1,
            'is_synthetic_demo': True
        }
    )
    # Generate real DICOM file
    dcm_path_1 = generate_synthetic_dicom_file(
        patient=patients['UHID-2026-00104'],
        procedure=procs['RAD-XR-CHEST'],
        study_uid=study_1.study_instance_uid,
        accession_no=study_1.accession_number,
        modality='DX'
    )
    study_1.dicom_file_path = dcm_path_1
    study_1.save()

    # Approved Radiology Report
    rad_rep_1, _ = RadiologyReport.objects.get_or_create(
        study=study_1,
        defaults={
            'report_number': 'REP-RAD-20261012-0041',
            'version': 1, 'status': RadiologyReportStatus.APPROVED,
            'reporting_radiologist': 'Dr. Arthur Sterling, MD',
            'clinical_indication': 'Fever and dyspnea. Rule out community-acquired pneumonia.',
            'examination_technique': 'Upright posteroanterior and lateral projections of the chest.',
            'findings': 'Frontal and lateral chest radiographs demonstrate dense consolidation within the right middle lobe with visible air bronchograms. Cardiac silhouette and cardiothoracic ratio are within normal limits. Trachea is midline. Costophrenic angles are sharp without pleural effusion. No pneumothorax. Osseous structures intact.',
            'impression': 'Acute right middle lobe lobar consolidation, findings consistent with community-acquired pneumonia.',
            'recommendations': 'Clinical correlation and follow-up radiograph in 4-6 weeks post antimicrobial therapy to verify resolution.',
            'approved_by': 'Dr. Arthur Sterling, MD',
            'approved_at': timezone.now() - timedelta(minutes=45)
        }
    )

    # Study 2: CT Head without Contrast (Awaiting Interpretation)
    rad_ord_2, _ = ImagingOrder.objects.get_or_create(
        order_number='ORD-RAD-20261012-CT02',
        defaults={
            'tenant': tenant_a, 'branch': branch_a1, 'patient': patients['UHID-2026-00102'],
            'accession_number': 'RAD-261012-CT88',
            'ordering_clinician': 'Dr. Catherine Ross', 'priority': 'ROUTINE',
            'status': ImagingOrderStatus.REPORT_PENDING, 'clinical_history': 'Recurrent headaches, rule out intracranial lesion',
            'ordered_at': timezone.now() - timedelta(hours=2),
            'completed_at': timezone.now() - timedelta(minutes=30)
        }
    )
    rad_item_2, _ = ImagingOrderItem.objects.get_or_create(
        order=rad_ord_2, procedure=procs['RAD-CT-BRAIN-NC'],
        defaults={'price_at_order': 290.00}
    )
    study_2, _ = ImagingStudy.objects.get_or_create(
        order_item=rad_item_2,
        defaults={
            'patient': patients['UHID-2026-00102'],
            'study_instance_uid': '1.2.840.10008.5.1.4.1.1.20261012.1002',
            'accession_number': 'RAD-261012-CT88',
            'modality_type': ModalityType.CT,
            'study_description': 'CT Head / Brain without IV Contrast',
            'performing_technologist': 'Marcus Vance, RT(R)',
            'series_count': 1, 'instance_count': 1,
            'is_synthetic_demo': True
        }
    )
    dcm_path_2 = generate_synthetic_dicom_file(
        patient=patients['UHID-2026-00102'],
        procedure=procs['RAD-CT-BRAIN-NC'],
        study_uid=study_2.study_instance_uid,
        accession_no=study_2.accession_number,
        modality='CT'
    )
    study_2.dicom_file_path = dcm_path_2
    study_2.save()

    RadiologyReport.objects.get_or_create(
        study=study_2,
        defaults={
            'report_number': 'REP-RAD-20261012-0042',
            'version': 1, 'status': RadiologyReportStatus.DRAFT,
            'reporting_radiologist': 'Dr. Arthur Sterling, MD',
            'clinical_indication': 'Chronic cephalalgia evaluation',
            'examination_technique': 'Helical axial non-contrast CT acquisition of the neurocranium.',
            'findings': 'Ventricular system, sulci, and basal cisterns are symmetric and age-appropriate. Gray-white matter differentiation is preserved. No acute intracranial hemorrhage, mass effect, or midline shift.',
            'impression': 'Normal non-contrast head CT without acute intracranial pathology.'
        }
    )

    print("--- [SEEDING COMPLETED SUCCESSFULLY] ---")
    print(f"Tenants: {Tenant.objects.count()} | Patients: {PatientContract.objects.count()} | Lab Tests: {LabTest.objects.count()}")
    print(f"Lab Orders: {LabOrder.objects.count()} | Specimens: {Specimen.objects.count()} | Lab Reports: {LabReport.objects.count()}")
    print(f"Rad Procedures: {ImagingProcedure.objects.count()} | Imaging Orders: {ImagingOrder.objects.count()} | DICOM Studies: {ImagingStudy.objects.count()}")

if __name__ == '__main__':
    seed()
