# Hospital Management System (HMS) - Multi-Tenant Healthcare SaaS

Welcome to the **Hospital Management System (HMS)** monorepo, a multi-tenant healthcare enterprise platform.

## Architecture Overview

This platform is structured into modular domains maintained collaboratively by 7 functional domain teams:

- **Member 1 (Platform & SaaS Admin)**: Multi-hospital tenants, branches, RBAC, subscription tiers, audit logging.
- **Member 2 (Patient Management & Appointments)**: Patient Master Records (MPI), MRN generation, duplicate resolution, appointment scheduling, queue/token engine, OPD/IPD admission & bed management, patient portal.
- **Member 3 (Clinical & EMR/EHR)**: Doctor/nurse workspaces, clinical encounters, vitals, e-prescriptions, nursing handovers.
- **Member 4 (Laboratory & Radiology)**: Lab order processing, specimen tracking, DICOM studies, imaging viewer integration.
- **Member 5 (Pharmacy & Inventory)**: Drug formulary, batch/expiry tracking, dispensing, purchase orders.
- **Member 6 (Billing & Finance)**: Service catalogue, itemized invoicing, payment gateways, insurance claims, GST compliance.
- **Member 7 (Mobile/Portals, QA & Release)**: Patient/doctor portals, WebRTC teleconsultation, E2E testing, CI/CD.

---

## Member 2 Module Scope & Responsibilities

The **Patient Management & Appointments** module is responsible for the foundational lifecycle of patient care:

1. **Master Patient Index (MPI) & Profiles**:
   - Unique alphanumeric Medical Record Number (MRN) format per tenant.
   - Comprehensive demographic, contact, and identification details.
   - Algorithmic duplicate detection (Exact Match, Levenshtein Distance, Metaphone/Phonetic indexing).
   - Safe merge workflows preserving historical audits and unmerge capabilities.
2. **Scheduling & Availability Engine**:
   - Doctor recurring schedules, special shifts, leave rules, and break buffers.
   - Slot calculation engine avoiding cross-branch conflicts.
   - High-concurrency booking mechanism with DB-level row locks (`select_for_update`) preventing race-condition double bookings.
3. **Queue & Token Management (OPD)**:
   - Walk-in tokens and scheduled tokens with prioritized queues.
   - Real-time queue progression (Waiting -> In Consultation -> Completed / No-Show).
4. **Inpatient Department (IPD) & Bed Allocation**:
   - Ward, room, and bed state management (Available, Occupied, Cleaning, Maintenance).
   - Admission orders, room transfers, nursing handovers, discharge clearance state machine.
5. **Patient Portal & Notifications**:
   - Patient self-service registration, appointment booking, and dispatching hooks.

---

---

## Member 3 Module Scope & Responsibilities (Clinical Management & EMR/EHR)

The **Clinical Management & EMR/EHR** module forms the core diagnostic and treatment documentation engine of the hospital system:

### 1. Doctor & Physician Workstation (`DoctorWorkspace.tsx`)
- Structured SOAP clinical note authoring (Subjective, Objective, Assessment, Plan).
- Cryptographic encounter sign-off with SHA-256 tamper-evident integrity hashes.
- Absolute immutability enforcement: signed records cannot be overwritten; amendments are recorded via versioned addenda.
- Embedded clinical calculators: CHA2DS2-VASc, CKD-EPI eGFR, CURB-65 pneumonia severity score.
- Integrated ICD-10 diagnostic search against master clinical registry (2,250 codes).
- Electronic Prescription (eRx) builder with automated allergen cross-checks.

### 2. Inpatient Nursing Station & Console (`NursingStationConsole.tsx`)
- Bedside telemetry flowsheet tracking: BP, Heart Rate, Respiration, Temp (°C), SpO2, AVPU, Pain Score.
- Automated Modified Early Warning Score (MEWS) engine with real-time clinical escalation triggers.
- Fluid Balance monitoring: strict intake (oral + IV) vs output (urine + drains) volume accounting.
- electronic Medication Administration Record (eMAR) with bedside 5-rights verification.
- Evidence-based SBAR Shift Handover protocols (Situation, Background, Assessment, Recommendation).

### 3. Longitudinal Patient EMR Chart Viewer (`PatientEMRViewer.tsx`)
- Comprehensive chronological timeline of consultations, clinical diagnoses, active prescriptions, and vitals.
- Allergies banner with color-coded severity grading (Mild, Moderate, Severe, Life-Threatening Anaphylaxis).
- Audit trail displaying original notes alongside versioned addenda with author and timestamp verification.

### 4. Master Clinical Registries & Safety Datasets (>1,30,000 LOC)
- `icd10Registry.ts` (49,530 lines): 2,250 ICD-10 diagnostic entries spanning 21 WHO chapters.
- `drugInteractions.ts` (21,631 lines): 1,200 drug-drug interaction safety rules (Major, Moderate, Minor) with clinical management guidance.
- `clinicalTemplatesRegistry.ts` (18,632 lines): 600 specialty documentation templates (Cardiology, Neurology, Surgery, Pediatrics, etc.).
- `nursingCarePlans.ts` (16,824 lines): 600 NANDA-I/NIC/NOC evidence-based nursing care plans.
- `clinicalAuditStudy.ts` (22,535 lines): 1,500 longitudinal clinical cases for quality audit and research benchmarking.
- `clinicalCalculators.ts` (2,093 lines): Validated clinical risk scores and medical formulas.

### 5. Backend REST API Endpoints (`/api/clinical/`)
| Method | Endpoint | Description |
|---|---|---|
| `GET / POST` | `/api/clinical/encounters/` | Encounter listings & SOAP documentation |
| `POST` | `/api/clinical/encounters/{id}/sign/` | Finalize & cryptographically lock encounter |
| `POST` | `/api/clinical/encounters/{id}/amend/` | Append versioned addendum to signed encounter |
| `GET` | `/api/clinical/encounters/patient_timeline/` | Longitudinal EMR consultation timeline |
| `GET / POST` | `/api/clinical/diagnoses/` | ICD-10 encounter diagnostic coding |
| `GET / POST` | `/api/clinical/allergies/` | Patient allergy profiles & severity tracking |
| `POST` | `/api/clinical/allergies/check_conflict/` | Automated medication-allergy conflict check |
| `GET / POST` | `/api/clinical/prescriptions/` | Electronic prescriptions & orders |
| `GET / POST` | `/api/clinical/nursing-observations/` | Flowsheet vitals & automated MEWS scoring |
| `GET / POST` | `/api/clinical/fluid-balances/` | Fluid balance intake vs output monitoring |
| `GET / POST` | `/api/clinical/emar/` | eMAR scheduled and administered doses |
| `POST` | `/api/clinical/emar/{id}/administer/` | 5-rights bedside medication administration |
| `GET / POST` | `/api/clinical/sbar-handovers/` | SBAR shift handover documentation |
| `GET / POST` | `/api/clinical/discharge-summaries/` | Inpatient discharge summaries & doctor sign-off |
| `GET / POST` | `/api/clinical/referrals/` | Inter-departmental clinical consultations |
| `GET / POST` | `/api/clinical/templates/` | Specialty documentation note templates |

---

## Technology Stack

- **Backend**: Python 3.10+, Django 4.2+ / Django REST Framework, PostgreSQL / SQLite.
- **Frontend**: Next.js / React 18, TypeScript, Tailwind CSS, Lucide Icons.
- **Testing**: `pytest`, `pytest-django`, Node test runner.
- **Documentation**: OpenAPI 3.0 / Swagger (`/api/docs/`).

---

## Development Setup

### Backend Setup
```bash
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
pytest
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm test
npm run build
npm run dev
```

