# Hospital Management System (HMS) — Multi-Tenant SaaS Platform

## Member 6 Workstream: Billing, Payments, Insurance & Financial Management

A production-grade, multi-tenant healthcare SaaS billing, insurance, accounting, and financial integrity system designed for modern multi-hospital networks.

---

### Scope & Team Allocation

This repository represents the **Member 6** implementation pod within the 7-member HMS architectural framework:
- **Member 6 Ownership:** Billing Management, Payment Processing, Reconciliation, Insurance Claims & Denial Workbench, GST/Tax Engine, Chart of Accounts & Double-Entry General Ledger, Accounts Receivable/Payable, Financial Period Closing, and Financial Integrity Monitor.
- **Contract Interfaces:** Clean decoupled stubs and interfaces are used for integration with Patient Records (M1), Clinical Encounters (M2/M3), Diagnostic Orders (M4), and Pharmacy Dispensing (M5).

---

### Key Capabilities of Member 6

1. **Hospital Billing Management:**
   - Multi-department itemized invoicing (OPD, IPD, Diagnostics, Pharmacy).
   - Strict invoice state machine (`DRAFT`, `ISSUED`, `PARTIALLY_PAID`, `PAID`, `OVERDUE`, `CANCELLED`).
   - Credit notes, line discounts, and automated balance calculation.
2. **Payment Processing & Reconciliation:**
   - Multi-tender transactions (Cash, Card, UPI, Wire Transfer).
   - Idempotency key protection preventing double charges.
   - Smart reconciliation engine matching settlement reports against recorded receipts.
   - Multi-tier refund requests with auditable approval workflows.
3. **Insurance & Claims Management:**
   - Payer and TPA registries, policy coverage verification.
   - Adjudication pipeline with **Denial Workbench** for deficiency tracking and resubmissions.
4. **Indian GST & Tax Engine:**
   - Dynamic intra-state (CGST + SGST) vs. inter-state (IGST) determination.
   - HSN/SAC codes and tax-exempt healthcare services.
5. **Double-Entry General Ledger & Period Closing:**
   - Configurable 5-category Chart of Accounts.
   - Invariant enforcement: $\sum Debit = \sum Credit$ on every journal entry.
   - Financial period closing with locking of historical accounting records.
6. **Financial Integrity Monitor & Unified Timelines:**
   - Real-time detection of unbalanced journals, duplicate references, and anomalous refunds.
   - Unified chronological timeline per invoice.

---

### Technology Stack

- **Backend:** Python 3.13+, Django 5+, Django REST Framework, drf-spectacular (OpenAPI).
- **Frontend:** React 18+, TypeScript, Vite, Tailwind CSS / modern CSS design system.
- **Database:** PostgreSQL (production) / SQLite (development & automated test suite).
- **Multi-Tenancy:** Partitioned database architecture scoped via tenant context (`X-Tenant-ID`).

---

---

## Installation

### 1. Backend Installation
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt || pip install django djangorestframework django-cors-headers drf-spectacular pytest pytest-django
```

### 2. Frontend Installation
```bash
cd frontend
npm install
cd ..
```

---

## Build

### 1. Build Frontend Application
```bash
cd frontend
npm run build
cd ..
```

### 2. Database Migrations & Static Files
```bash
python backend/manage.py migrate
python backend/manage.py seed_finance_data
```

---

## Run

### 1. Start Full Application (Entry Point)
```bash
python main.py
```

### 2. Run with Docker Compose
```bash
docker-compose up --build
```

### 3. Running Services Manually
- **Backend API:** `python backend/manage.py runserver 127.0.0.1:8000`
- **Frontend UI:** `cd frontend && npm run dev`
- **Web App:** Open `http://localhost:5173/` in your browser.
- **Swagger Docs:** Open `http://localhost:8000/api/docs/` in your browser.

---

## Testing

```bash
pytest -v
```

