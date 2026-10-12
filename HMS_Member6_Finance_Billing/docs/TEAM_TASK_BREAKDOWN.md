# HMS Team Task Breakdown & Module Assignment (7 Developers)

**Engineering Team Allocation for HMS SaaS:**

---

### Member 1 — Patient Registration & Master Records
- Issue #M1-01: Patient Master Index (PMI) and Unique Medical Record Number (MRN) generator.
- Issue #M1-02: Demographic records, emergency contacts, and relation maps.
- Issue #M1-03: Duplicate detection algorithms and patient record merger audit trail.
- Issue #M1-04: Patient document storage, ID uploads, and consent tracking.

### Member 2 — Appointments, OPD & IPD Management
- Issue #M2-01: Doctor scheduling, recurring availability, and leave blackout periods.
- Issue #M2-02: Appointment booking, token queue generator, and race-condition locking.
- Issue #M2-03: OPD triage intake, vital stations, and consultation check-in.
- Issue #M2-04: IPD ward management, bed allocation grid, and admission/discharge workflows.

### Member 3 — EMR/EHR & Clinical Documentation
- Issue #M3-01: Doctor clinical encounter notes and structured templates.
- Issue #M3-02: Diagnosis encoding (ICD-10 reference catalogues).
- Issue #M3-03: Electronic prescription orders and vitals longitudinal timeline.
- Issue #M3-04: Signed clinical document amendments and audit-versioned revisions.

### Member 4 — Laboratory & Radiology Workflows
- Issue #M4-01: Diagnostic test directory and standardized reference intervals.
- Issue #M4-02: Specimen barcoding, collection logs, and sample rejection workflows.
- Issue #M4-03: Lab technician result entry, critical alert flagging, and pathologist signing.
- Issue #M4-04: Radiology study accessioning, DICOM viewer integration, and PACS metadata links.

### Member 5 — Pharmacy & Inventory Management
- Issue #M5-01: Drug formulary, generic brands, dosages, and contraindication notices.
- Issue #M5-02: Prescription dispense queue, partial dispensing, and expiry batch tracking.
- Issue #M5-03: Purchase orders, supplier goods receipt notes (GRN), and stock ledger.
- Issue #M5-04: Departmental inventory transfers and transactional concurrency control.

### MEMBER 6 (ACTIVE SPRINT FOCUS) — Billing, Payments, Insurance & Accounting
- **Issue #M6-01:** Hospital Billing Management, Itemized Invoices (OPD/IPD/Lab/Rad/Pharm), Service Catalogue & Price Lists.
- **Issue #M6-02:** Payment Processing, Multi-Method Recording (Cash/Card/UPI/Wire), Receipts, Idempotency & Partial Payments.
- **Issue #M6-03:** Refund Management Lifecycle (Request, Approval, Processing) & Audit Controls.
- **Issue #M6-04:** Smart Payment Reconciliation, Bank/Gateway Settlement Batch Matching & Discrepancy Detection.
- **Issue #M6-05:** Insurance Payers & Policies, Pre-Authorization Tracking, and Claims Adjudication.
- **Issue #M6-06:** Insurance Claim Denial Workbench, Rejection Code Analytics, and Resubmission Tracking.
- **Issue #M6-07:** GST Tax Engine, Intra-State (CGST+SGST) vs. Inter-State (IGST) Calculation, HSN/SAC Codes & GSTR Reports.
- **Issue #M6-08:** Chart of Accounts, General Ledger, and Automated Double-Entry Balancing Engine.
- **Issue #M6-09:** Accounts Receivable Aging Analysis (0-30, 31-60, 61-90, 90+ days) and Accounts Payable Management.
- **Issue #M6-10:** Financial Integrity Monitor (Unbalanced Entries, Duplicate References, Anomaly Alerts).
- **Issue #M6-11:** Financial Period Closing Workflow, Hardening, and Period Lock Enforcements.
- **Issue #M6-12:** Unified Financial Timeline per Invoice and PDF/CSV Export Generators.
- **Issue #M6-13:** Complete Frontend Financial UI System (18 dedicated pages and interactive components).
- **Issue #M6-14:** Automated Test Suite for Decimal Safety, Double-Entry Invariants, Tenant Isolation & Workflows.

### Member 7 — Telemedicine, Portals & Integration Platform
- Issue #M7-01: Patient self-service portal (bill viewing, appointment booking, report access).
- Issue #M7-02: Doctor consultation portal and schedule views.
- Issue #M7-03: WebRTC video consultation rooms, STUN/TURN configuration, and waiting rooms.
- Issue #M7-04: Multi-channel notifications (SMS/Email stubs) and staff task escalation queue.
