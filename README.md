# Hospital Management System (HMS) - Multi-Tenant Healthcare Enterprise Platform

Welcome to the **Hospital Management System (HMS)** enterprise monorepo, a unified multi-tenant healthcare software-as-a-service (SaaS) platform built to power hospital networks, specialized clinics, and academic medical centers.

---

## Architecture & Team Domain Modules

The platform is structured into modular domains maintained collaboratively by the 7 engineering domain teams:

- **Member 1 (Platform & Multi-Tenant Core)**: Multi-hospital tenants, branches, RBAC, domain routing, subscription tiers, audit logging.
- **Member 2 (Patient Management & Appointments)**: Patient Master Index (MPI), MRN generation, duplicate resolution, appointment scheduling, queue/token engine, OPD/IPD admission & bed management, patient portal.
- **Member 3 (Clinical Management & EMR/EHR)**: Doctor & nurse workstations, SOAP clinical encounters, bedside vitals flowsheets, e-prescriptions, clinical safety calculators, SBAR handovers, eMAR.
- **Member 4 (Laboratory & Radiology — LIS/RIS/PACS)**: CLIA/CAP lab orders, specimen tracking, LOINC test catalog, diagnostic reports, DICOMweb PS3.18 PACS integration, interactive HTML5 medical imaging viewer, and radiation dose monitoring.
- **Member 5 (Pharmacy & Inventory)**: WHO essential drug formulary, cold chain monitoring, batch & FEFO expiry tracking, electronic dispensing, purchase orders, narcotic logs.
- **Member 6 (Billing, Finance & Revenue Cycle)**: Departmental tariffs, procedural fee schedules, insurance claims workbench, GST compliance, double-entry general ledger, doctor consultation revenue sharing.
- **Member 7 (Portals, Telemedicine & Release QA)**: Patient self-service portal, WebRTC teleconsultation suite, cross-module E2E integration test suite, CI/CD automated validation.

---

## Delivered Domain Capabilities

### 1. Core & Multi-Tenant Foundation (Member 1)
- Header-based tenant resolution (`X-Tenant-ID`, `X-Tenant-Code`, `X-Branch-ID`).
- Strict row-level tenant boundary isolation across all relational tables.
- Role-Based Access Control (RBAC) with audit logs for HIPAA/CLIA compliance.

### 2. Patient Management & Appointments (Member 2)
- **Master Patient Index (MPI)**: Unique alphanumeric Medical Record Numbers (MRN) per tenant with algorithmic duplicate detection (Levenshtein + phonetic indexing).
- **Scheduling Engine**: Doctor recurring availability, shift buffers, leave management, and row-level concurrency lock booking (`select_for_update`).
- **OPD Queue & Token System**: Walk-in and scheduled priority tokens.
- **IPD Admissions & Bed Allocation**: Ward, room, and bed occupancy states (Available, Occupied, Cleaning, Maintenance) with discharge clearance reconciliation.

### 3. Clinical Management & EMR/EHR (Member 3)
- **Doctor Workstation (`DoctorWorkspace.tsx`)**: SOAP notes, cryptographic SHA-256 tamper-evident sign-off, immutable versioned amendments, and validated risk calculators (CHA2DS2-VASc, CKD-EPI, CURB-65).
- **Nursing Station (`NursingStationConsole.tsx`)**: Bedside vitals, automated Modified Early Warning Score (MEWS), intake/output fluid balance, and 5-rights eMAR verification.
- **Clinical Registries**: 2,250 ICD-10 diagnostic entries, 1,200 drug-drug interaction rules, 600 specialty documentation templates, and 600 NANDA-I care plans.

### 4. Laboratory (LIS) & Radiology (RIS & PACS) (Member 4)
- **Laboratory Information System (LIS)**: Real-time dashboard, LOINC test catalogue, duplicate order prevention guards, specimen custody tracking, barcode generation, technician result entry, supervisor validation, consultant pathologist digital sign-off, and automated ReportLab PDF reports.
- **Radiology Information System (RIS)**: Equipment modality suites (DX, CT, MR, US), Modality Worklist (MWL) PS3.4 query feeds, and RSNA structured reporting.
- **DICOMweb PACS & Medical Image Viewer**: Authentic DICOM Part 10 dataset streaming (`pydicom`), HTML5 canvas viewer with Window/Level presets (Bone, Lung, Brain, Soft Tissue), pan, zoom, invert, and caliper distance measurement tools.
- **Safety & Alerts**: STAT urgency triage, critical panic value telephone escalation protocol, contrast-induced nephropathy eGFR clearance screening, and AAPM CTDI/DLP radiation dose tracking.

### 5. Pharmacy & Inventory Management (Member 5)
- WHO Model Formulary catalog loader with ATC categorization and dosage units.
- Batch-level First-Expiry-First-Out (FEFO) dispensing with automated stock lot deduction.
- Real-time clinical safety checks (drug-drug, drug-allergy, pediatric dosage limits).
- Scheduled narcotic register with dual-witness digital sign-offs and shift reconciliations.

### 6. Billing, Invoicing & Insurance (Member 6)
- Comprehensive procedural tariff schedules across surgical, diagnostic, and specialty departments.
- Itemized billing and multi-payer settlement breakdown (Cash, Card, Empaneled Insurance, Corporate TPA).
- Automated statutory GST tax compliance and accounts receivable / accounts payable general ledger.

### 7. Telemedicine & Patient Portals (Member 7)
- Patient self-service appointment booking and timeline history.
- WebRTC video teleconsultation room allocation adapter.
- Production release workflows and end-to-end integration test runners.

---

## Technology Stack

- **Backend**: Python 3.10+, Django 4.2+ / Django REST Framework, SQLite / PostgreSQL, ReportLab, PyDicom.
- **Frontend**: React 18, Vite, TypeScript, Tailwind CSS, Lucide Icons, HTML5 Medical Canvas.
- **API Documentation**: OpenAPI 3.0 / Swagger UI (`/api/docs/`) & ReDoc (`/api/redoc/`).
- **Testing**: `pytest`, `pytest-django`, Node test runner.

---

## Quick Start & Local Execution

### 1. Automated 1-Click Launch (Windows)

Run the included launcher script:
```powershell
.\start.ps1
```
Or with batch file:
```cmd
start.bat
```

This automatically:
1. Applies all database migrations across all member apps.
2. Seeds initial multi-tenant test data and clinical records.
3. Launches the Django REST API backend on `http://127.0.0.1:8000`.
4. Starts the Vite Frontend Portal on `http://localhost:5173`.

### 2. Manual Launch Steps

#### Backend
```cmd
cd backend
python manage.py migrate
python seed_hms_data.py
python manage.py runserver 127.0.0.1:8000
```
- Interactive Swagger UI: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- ReDoc API Documentation: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
- Member 4 LIS/RIS Console: [http://127.0.0.1:8000/lis-ris/](http://127.0.0.1:8000/lis-ris/)

#### Frontend Portal
```cmd
cd frontend
npm install
npm run dev
```
- Open in browser: [http://localhost:5173](http://localhost:5173)

---

## Running Automated Tests

Run the full cross-domain backend test suite:
```cmd
cd backend
pytest -v
```

Run Member 4 LIS/RIS automated test suite:
```cmd
cd backend
pytest tests/test_member4_lis_ris.py -v
```
