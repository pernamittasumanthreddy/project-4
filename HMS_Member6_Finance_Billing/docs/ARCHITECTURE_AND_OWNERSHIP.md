# HMS System Architecture & Module Ownership Matrix

**Project:** Multi-Tenant SaaS Hospital Management System (HMS)  
**Standard Architecture & Team Division:** 7-Member Engineering Pod  
**Scope Definition:** Strict Module Boundaries with Member 6 Exclusive Ownership  

---

## 1. System Architecture Diagram

```
                     ┌────────────────────────────────────────────────────────┐
                     │            Multi-Tenant Web Client (React + TS)        │
                     │  - Member 6 UI: 18 Specialized Financial Pages / Views │
                     └──────────────────────────┬─────────────────────────────┘
                                                │ HTTPS / REST (X-Tenant-ID)
                                                ▼
                     ┌────────────────────────────────────────────────────────┐
                     │           API Gateway / Django REST Framework          │
                     │  - Tenant Scoping & RBAC (Role-Based Access Control)   │
                     │  - OpenAPI / Swagger Documentation (drf-spectacular)   │
                     └──────┬───────────────────┬───────────────────────┬─────┘
                            │                   │                       │
      ┌─────────────────────▼────────┐ ┌────────▼────────────────┐ ┌────▼─────────────────────┐
      │  External Member Contracts   │ │  Member 6 Core Engine   │ │ Financial Integrations   │
      │  (Read-only references)      │ │  - Hospital Billing     │ │ - Tax Engine (Indian GST)│
      │  - Patients (Member 1)       │ │  - Payment & Reconcil.  │ │ - Insurance Claims & TPA │
      │  - Encounters (Member 2)     │ │  - Denial Workbench     │ │ - Smart Reconciliation   │
      │  - Clinical Orders (M3)      │ │  - Double-Entry GL      │ │ - Payment Gateways       │
      │  - Lab/Rad Orders (M4)       │ │  - Financial Integrity  │ │ - Period Closing Engine  │
      │  - Pharmacy Dispense (M5)    │ │  - Auditable Timelines  │ │ - Export Engines (CSV/PDF)
      └──────────────────────────────┘ └────────┬────────────────┘ └──────────────────────────┘
                                                │
                                                ▼
                     ┌────────────────────────────────────────────────────────┐
                     │        PostgreSQL / SQLite Database Layer              │
                     │  - Shared schema with enforced tenant partitioning     │
                     │  - Strict Foreign Keys, Unique Indexes, Audit Tables   │
                     │  - Decimal Precision (28, 4) for monetary figures      │
                     └────────────────────────────────────────────────────────┘
```

---

## 2. 7-Member Module Ownership Matrix

| Member | Assigned Domain | Status / Boundary Rule |
| :--- | :--- | :--- |
| **Member 1** | Patient Registration & Master Records | Stubs/Contracts only. Outside Member 6 scope. |
| **Member 2** | Appointments, OPD Triage & IPD Bed Management | Stubs/Contracts only. Outside Member 6 scope. |
| **Member 3** | EMR/EHR & Clinical Workflows | Stubs/Contracts only. Outside Member 6 scope. |
| **Member 4** | Laboratory & Radiology Workflows | Stubs/Contracts only. Outside Member 6 scope. |
| **Member 5** | Pharmacy Catalogue & Drug Inventory | Stubs/Contracts only. Outside Member 6 scope. |
| **MEMBER 6 (ACTIVE)** | **Hospital Billing, Payment Processing, Insurance Claims, GST & Tax Engine, Double-Entry Accounting, Financial Analytics & Integrity Monitor** | **EXCLUSIVELY IMPLEMENTED BY THIS WORKSTREAM** |
| **Member 7** | Telemedicine, Portals & Notification System | Stubs/Contracts only. Outside Member 6 scope. |

---

## 3. Member 6 Detailed Functional Areas

### 6.1 Hospital Billing Management
- Itemized invoicing for OPD consultations, IPD ward stays, laboratory investigations, radiology scans, and pharmacy items.
- Configurable service catalogue and tiered hospital price lists.
- Invoice state machine: `DRAFT` ➔ `ISSUED` ➔ `PARTIALLY_PAID` ➔ `PAID` / `OVERDUE` / `CANCELLED`.
- Line-item discounts, concessions, and auditable credit notes.

### 6.2 Payment Processing & Reconciliation
- Multi-mode payment recording: Cash, Credit/Debit Card, Wire Transfer, Digital/UPI.
- Partial payment support, receipt printing numbers, idempotency verification.
- Multi-stage refund lifecycle (`REQUESTED` ➔ `APPROVED` ➔ `PROCESSED` / `REJECTED`).
- Smart reconciliation matching internal payments to external settlement batches.

### 6.3 Insurance & Claims Management
- Payer and TPA registry (Private, Corporate, Government schemes like CGHS/Ayushman Bharat).
- Policy validation, pre-authorization tracking.
- Adjudication state transitions (`SUBMITTED`, `PENDING_REVIEW`, `APPROVED`, `PARTIALLY_APPROVED`, `REJECTED`, `SETTLED`).
- **Insurance Claim Denial Workbench**: Specific rejection root-cause codes, deficiency documentation checklist, resubmission tracking.

### 6.4 GST & Tax Configuration
- Indian GST compliance framework: CGST (Central), SGST (State), IGST (Integrated).
- Intra-state vs. inter-state tax categorization based on billing entity state and patient state.
- HSN / SAC code tax mapping, tax-inclusive vs. tax-exclusive line pricing, and GSTR summaries.

### 6.5 Accounting & Financial Management
- Configurable Chart of Accounts (5 Root Categories: Assets, Liabilities, Equity, Revenue, Expenses).
- Automated double-entry bookkeeping engine (`sum(Debit) == sum(Credit)` strictly enforced).
- General ledger, accounts receivable aging (0-30, 31-60, 61-90, 90+ days), and accounts payable records.
- Financial period closing with pre-closing sanity checks and audit log preservation.

### 6.6 Financial Analytics, Integrity Monitor & Timelines
- Live revenue analytics: Billed, collected, outstanding, and claim conversion rate.
- Department-wise revenue attribution (OPD, IPD, Lab, Radiology, Pharmacy).
- Real-time **Financial Integrity Monitor**: Automated scans for unbalanced journals, duplicate transaction references, anomalous refunds, and reconciliation gaps.
- **Unified Financial Timeline**: End-to-end chronological audit trail for every invoice.
