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

## Technology Stack

- **Backend**: Python 3.10+, Django 4.2+ / Django REST Framework, PostgreSQL.
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Lucide Icons.
- **Testing**: `pytest`, `pytest-django`, Jest / React Testing Library.
- **Documentation**: OpenAPI 3.0 / Swagger.

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
python manage.py runserver
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
