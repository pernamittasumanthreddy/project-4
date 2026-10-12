# CareTrust Health System — HMS Multi-Tenant Enterprise SaaS

> **Enterprise Multi-Tenant Healthcare Platform — Member 7 Delivery**  
> **Patient Portal • Doctor Portal • Telemedicine & WebRTC • Notifications • Automated QA • Cross-Module Integration**  
> *100% Local Execution • Zero Paid External API Keys • 16/16 Automated Tests Passed*

---

## 1. System Identity & Overview

CareTrust HMS is a production-grade multi-tenant healthcare platform built with **Python 3.12, Django 6, Django REST Framework, React 18, TypeScript, and Vite**.

This repository contains the complete **Member 7** module delivery integrating all 7 team domains:
1. **Patient Portal**: Personalized dashboard, real-time appointment booking wizard, longitudinal medical records, approved lab/radiology viewer, itemized invoice viewer with sandbox payments, profile management.
2. **Doctor Portal**: Clinician dashboard, daily and weekly agenda schedule, clinical consultation workstation (SOAP notes, vitals recording, ICD-10 diagnosis, prescription writing, digital sign-off lock).
3. **Telemedicine Suite**: Browser-to-browser WebRTC consultation room with public Google STUN fallback, pre-join camera/mic device checks, in-call chat, doctor clinical quick notes, and session lifecycle tracking.
4. **Notification Center**: Real-time in-app notifications, unread badges, event deduplication, and safe local Email/SMS delivery adapters.
5. **Cross-Module Integration**: Clean integration contracts with Member 1 (Auth/Tenancy), Member 2 (Appointments), Member 3 (EMR), Member 4 (Diagnostics), Member 5 (Pharmacy), and Member 6 (Billing).
6. **Automated QA & CI/CD**: 16 unit, integration, and E2E test cases passing with 100% success rate, alongside GitHub Actions workflows.

---

## 2. Pre-Configured Demo Personas (1-Click Switcher)

The application includes a persistent top bar enabling instant 1-click switching between pre-seeded personas:

| Role | Username | Persona Name | Clinical Domain / Status |
|---|---|---|---|
| **Doctor** | `doctor_chen` | Dr. Sophia Chen, MD FACC | Senior Interventional Cardiologist (CareTrust Main) |
| **Doctor** | `doctor_vance` | Dr. Marcus Vance, MD FCCP | Chief Pulmonologist & Critical Care (North Wing) |
| **Patient** | `patient_priya` | Priya Sharma | Cardiac Patient (`MRN-2026-90412`, Penicillin Allergy) |
| **Patient** | `patient_david` | David Miller | Chronic Pulmonology Patient (`MRN-2026-88104`) |
| **Hospital Admin** | `hospital_admin` | Sarah Jenkins | Hospital System Administrator |

---

## 3. Quick Start & Local Execution

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Node.js v18+ and npm

### Option A: 1-Click Launch (Windows)
Double-click `start.bat` or run:
```powershell
.\start.ps1
```

### Option B: Manual Setup

#### 1. Backend Setup
```bash
# Apply database migrations
python backend/manage.py migrate

# Seed realistic multi-tenant data
python backend/seed_hms_data.py

# Start Django development server
python backend/manage.py runserver 127.0.0.1:8000
```

#### 2. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Start Vite development server
npm run dev
```

Visit **`http://localhost:5173`** in your web browser!

---

## 4. Automated Test Suite Execution

Run all 16 tests covering multi-tenant isolation, RBAC security, patient portal filtering, doctor portal locking, telemedicine signaling, notifications, and E2E lifecycle:

```bash
python backend/manage.py test tests
```

**Output**:
```
Ran 16 tests in 0.884s
OK
```

---

## 5. Security & Privacy Guarantees
- **Multi-Tenant Scoping**: All records are logically isolated by tenant UUIDs.
- **Suppression of Draft Lab Reports**: Unapproved diagnostic reports are strictly hidden from patient portal views.
- **Signed Encounters Lock**: Finalized clinical notes cannot be edited without authorization.
- **Zero Hardcoded Secrets**: Operates without any paid vendor API keys.
