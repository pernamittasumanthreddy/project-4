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

## Dependencies

The platform requires Python 3.10+ and Node.js 18+ (or Docker).

- **Backend Dependencies**: Listed in [`requirements.txt`](file:///requirements.txt)
  - `Django>=4.2`
  - `djangorestframework>=3.14`
  - `django-cors-headers>=4.0`
  - `pydicom>=2.4.0`
  - `reportlab>=4.0.0`
  - `pytest>=7.4`
  - `pytest-django>=4.5`
- **Frontend Dependencies**: Listed in [`package.json`](file:///package.json) and locked in [`package-lock.json`](file:///package-lock.json)
  - `react>=18.2.0`, `react-dom>=18.2.0`
  - `lucide-react`, `recharts`
  - `vite>=6.0`, `typescript>=5.0`, `tailwindcss>=3.4`

---

## Installation

### 1. Environment Setup

```bash
# Clone the repository
git clone https://github.com/pernamittasumanthreddy/project-4.git
cd project-4

# Setup Python Virtual Environment
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Install Python backend dependencies
pip install -r requirements.txt

# Install Node frontend dependencies
npm install
cd frontend && npm install && cd ..
```

### 2. Database Migrations & Initial Seed

```bash
cd backend
python manage.py migrate
python seed_hms_data.py
cd ..
```

---

## Build

### Build Frontend Production Assets
```bash
# Using root npm command
npm run build

# Or directly in frontend
cd frontend
npm run build
cd ..
```

### Build Docker Container
```bash
docker build -t hms-enterprise:latest .
```

---

## Run

### Option A: 1-Click Launch (Recommended)
- **Windows PowerShell**:
  ```powershell
  .\start.ps1
  ```
- **Windows Command Prompt**:
  ```cmd
  start.bat
  ```
- **Python Unified Runner**:
  ```bash
  python main.py
  ```
- **Docker Compose**:
  ```bash
  docker compose up -d
  ```

### Option B: Manual Multi-Service Run
1. **Start Django Backend (Port 8000)**:
   ```bash
   cd backend
   python manage.py runserver 127.0.0.1:8000
   ```
2. **Start Vite Frontend Portal (Port 5173)**:
   ```bash
   cd frontend
   npm run dev
   ```

---

## Usage

1. **Enterprise Portal Web UI**: Navigate to [http://localhost:5173](http://localhost:5173).
   - Use the 15-role quick login selector to access any medical workstation (*Attending Physician*, *Nurse Console*, *Emergency Command*, *Pharmacy Workstation*, *Pathology LIS*, *Radiology PACS*, etc.).
2. **REST API & Swagger Documentation**: [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
3. **ReDoc Interactive Reference**: [http://127.0.0.1:8000/api/redoc/](http://127.0.0.1:8000/api/redoc/)
4. **PACS / DICOM Diagnostic Viewer**: [http://127.0.0.1:8000/lis-ris/](http://127.0.0.1:8000/lis-ris/)

---

## Multi-Role Grounded RAG Clinical Assistant (Member 3)

The platform embeds an **on-premise, zero-hallucination Retrieval-Augmented Generation (RAG)** clinical knowledge assistant available across all 15 hospital dashboards:

- **Hybrid Retrieval Architecture**: Combines **BM25 lexical search** with **Semantic Vector Embeddings** through **Reciprocal Rank Fusion (RRF)**.
- **Strict Role-Based Access Control (RBAC)**: Enforces document scope isolation (e.g. ICU Sepsis protocols for clinicians, Formulary SOPs for pharmacists, Pre-authorization rules for billing, and privacy guidelines for patients).
- **0% Hallucination Policy & Diagnostic Guardrails**: Rejects unverified medical claims and intercepts autonomous diagnostic/prescribing attempts with clinical advisories directing users to licensed providers.
- **Dual Execution Engine**:
  - **In-Browser Client Execution**: Instantaneous local retrieval (~10ms) with zero cloud network dependencies.
  - **Django REST API Endpoints**: Available at `/api/rag/query` and `/api/rag/evaluate` for external interoperability and automated test suites.

---

## 15 Role Workstations & Perspectives

Every hospital role has a dedicated workstation dashboard with customized clinical/operational tools and dedicated Logout buttons:

| # | Role Workstation | Primary User | Department Scope | Key Tools & Actions |
|---|---|---|---|---|
| 1 | **Doctor Workstation** | Dr. Marcus Vance, MD | Cardiology / IPD | SOAP consultations, EMR timeline, e-prescribing, CDS calculators, SHA-256 note locking |
| 2 | **Nursing Station** | Sarah Jenkins, RN | Intensive Care (ICU) | Bedside vitals, MEWS deterioration alerts, fluid balance flowsheet, eMAR 5-rights verification |
| 3 | **Emergency Command** | Dr. Robert Thorne, MD | Trauma Bay / ED | Manchester Triage System (MTS) Red/Orange triage, Code Blue/STEMI triggers, rapid transfer |
| 4 | **Hospital Administrator** | Dr. Arthur Pendelton | Administration | Hospital census, bed occupancy tracking, visitor protocols, incident management |
| 5 | **Super Admin** | Alexander Sterling | Governance | Multi-tenant isolation, cross-hospital branches, user credentialing, security audit logs |
| 6 | **Patient Portal** | Eleanor Vance | Inpatient / Outpatient | Health records, validated lab results, appointments, prescription refill requests |
| 7 | **Pharmacist Station** | Samuel Miller, RPh | Pharmacy Services | High-alert double checks, generic substitutions, narcotic logs, dispensing approval |
| 8 | **Laboratory Console** | Dr. Karen White, MD | Pathology & LIS | Specimen accessioning, LOINC test catalog, panic critical value readback (<30 min rule) |
| 9 | **Radiology & PACS** | Dr. Jonathan Blake, MD | Diagnostic Imaging | Modality worklist (CT/MRI/X-Ray), DICOMweb PS3.18 viewer, contrast eGFR clearance check |
| 10 | **Billing & Finance** | Claire Henderson | Revenue Cycle | Itemized billing, procedural fee schedules, GST invoices, deposit reconciliation |
| 11 | **Insurance & TPA** | Michael Chang | Claims & Insurance | EDI 278 pre-authorizations, EDI 837 claims submission, denial appeal tracking |
| 12 | **Human Resources** | Eleanor Davis | HR & Credentialing | Physician/nurse board licensing, BLS/ACLS renewals, mandatory annual compliance |
| 13 | **Department Manager** | Dr. Anthony Rossi | Surgical Tower | Operating theatre schedules, surgical staff rosters, equipment allocation |
| 14 | **Management Executive** | Victoria Sterling | Executive Board | High-level clinical quality metrics, bed utilization analytics, hospital revenue KPI |
| 15 | **Compliance Officer** | Jonathan Hayes | Compliance & Legal | HIPAA access audit trails, chart snooping detection, regulatory inspection reports |

---

## Running Automated Tests

- **Run all backend Django tests**:
  ```bash
  cd backend
  pytest -v
  ```
- **Run all frontend automated test suites** (Clinical EMR & Multi-RAG Benchmarks):
  ```bash
  cd frontend
  npm run test
  ```
- **Run dedicated RAG benchmark evaluation test**:
  ```bash
  cd frontend
  npm run test:rag
  ```
- **Run clinical management EMR test**:
  ```bash
  cd frontend
  npm run test:clinical
  ```

