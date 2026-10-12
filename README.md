# HMS SaaS — Member 4: Laboratory & Radiology Module
## Multi-Tenant Hospital Management System (HMS SaaS)

This module is developed independently for **Team Member 4** of the 7-member HMS engineering team. It contains the complete, production-grade **Laboratory Information System (LIS)** and **Radiology Information System (RIS)** with genuine DICOMweb PACS integration, multi-tenant database isolation, ReportLab PDF generation, and verified team integration contracts.

---

### Quick Start (Windows)

#### Option 1: 1-Click Launch
Double-click `run.bat` in this directory:
```cmd
run.bat
```
This automatically runs database migrations, seeds synthetic test datasets, starts the server on port 8000, and opens [http://localhost:8000/](http://localhost:8000/) in your browser.

#### Option 2: Command Line
```cmd
cd backend
py manage.py migrate
py seed_data.py
py manage.py runserver 127.0.0.1:8000
```
- Web Application: [http://localhost:8000/](http://localhost:8000/)
- OpenAPI / Swagger UI: [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)
- Redoc Documentation: [http://localhost:8000/api/redoc/](http://localhost:8000/api/redoc/)

---

### Automated Test Suite Execution

Run the complete test suite with `pytest`:
```cmd
cd backend
py -m pytest tests/test_member4_lis_ris.py -v
```

**Actual Test Results:**
```text
tests/test_member4_lis_ris.py::TestMember4LISModule::test_test_catalogue_and_reference_range_evaluation PASSED [ 12%]
tests/test_member4_lis_ris.py::TestMember4LISModule::test_order_creation_and_duplicate_prevention PASSED [ 25%]
tests/test_member4_lis_ris.py::TestMember4LISModule::test_specimen_collection_and_rejection_workflow PASSED [ 37%]
tests/test_member4_lis_ris.py::TestMember4LISModule::test_critical_result_alert_and_acknowledgement PASSED [ 50%]
tests/test_member4_lis_ris.py::TestMember4LISModule::test_result_approval_report_generation_and_billing_contract PASSED [ 62%]
tests/test_member4_lis_ris.py::TestMember4RISModule::test_imaging_order_scan_completion_and_dicom_generation PASSED [ 75%]
tests/test_member4_lis_ris.py::TestMember4RISModule::test_radiology_reporting_signoff_and_pdf PASSED [ 87%]
tests/test_member4_lis_ris.py::TestMultiTenantIsolation::test_tenant_data_isolation PASSED [100%]

======================== 8 passed, 3 warnings in 4.02s ========================
```

---

### Delivered Capabilities for Member 4

#### 1. Laboratory Information System (LIS)
- **Live Database-Backed Dashboard**: Live counts for orders today, awaiting collection, in lab, results pending validation, approved reports, critical alerts, and turnaround time metrics.
- **Configurable Test Catalogue**: LOINC codes, specimen requirements, container types, age/sex reference ranges, and critical limits.
- **Order Lifecycle & Accessioning**: Order creation with duplicate detection (prevents duplicate orders within 15 mins), accession numbering, priority flags (Routine/Urgent/STAT).
- **Specimen & Custody Tracking**: Barcode generation, collection timestamps, lab receipt, specimen rejection with mandatory reason, and recollection requests.
- **Result Entry & Validation**: Numeric/text results, automatic evaluation of abnormal/critical flags, technician notes, supervisor validation, and consultant pathologist sign-off.
- **Diagnostic Reports**: Accredited ReportLab PDF generation with hospital branding, versions, and electronic sign-off.
- **Critical Alerts & Escalation**: Life-threatening value alerts with clinician telephone readback verification.
- **TAT & Quality Analytics**: Workload by department, specimen rejection rates, and CSV audit export.

#### 2. Radiology Information System (RIS & PACS)
- **Modality Dashboard**: Equipment room suites (DX, CT, MR, US) and active order counts.
- **Modality Worklist (MWL)**: PS3.4 Scheduled Procedure Step (SPS) worklist query feeds.
- **Standard DICOMweb Server**: PS3.18 QIDO-RS and WADO-RS endpoints serving authentic DICOM Part 10 datasets via `pydicom`.
- **Medical Image Viewer**: Interactive HTML5 canvas viewer with HUD overlays, Window/Level adjustments, clinical presets (Bone, Soft Tissue, Lung, Brain), pan, zoom, invert, reset, and Caliper measurement tools (distance in mm).
- **Radiology Reporting Workstation**: Structured findings, impressions, recommendations, BI-RADS assessment scores, and ReportLab PDF downloads.

#### 3. Team Integration Contracts
- **Member 1 (Auth & Multi-Tenancy)**: `X-Tenant-Code` header scoping querysets.
- **Member 2 (Patient Registry)**: Foreign key demographic syncing (`PatientContract`).
- **Member 3 (Clinical Encounters)**: Clinical indications and order ingestion.
- **Member 6 (Billing & Insurance)**: Emits `BillingEventContract` upon pathologist or radiologist sign-off.
