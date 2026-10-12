# HMS Enterprise Multi-Tenant SaaS Platform — Architecture Specification

## 1. System Overview & Vision
The **CareTrust Hospital Management System (HMS)** is a professional, multi-tenant SaaS healthcare platform built to enterprise standards. It coordinates outpatient clinical workflows, virtual care delivery, laboratory diagnostic investigations, longitudinal electronic medical records (EMR), patient accounting, and multi-channel notification dispatch.

## 2. 7-Member Architectural Breakdown

| Member | Primary Domain | Status | Key Deliverables & API Boundaries |
|---|---|---|---|
| **Member 1** | Core Platform & SaaS Administration | Complete | Multi-tenant isolation middleware, custom user RBAC, hospital campuses, HIPAA audit logs (`/api/v1/core/`) |
| **Member 2** | Patient Registration & Appointment Scheduling | Complete | Doctor directories, departments, slot calculation engine, duplicate-booking prevention (`/api/v1/appointments/`) |
| **Member 3** | Clinical Encounters & Electronic Medical Records | Complete | SOAP consultation notes, ICD-10 diagnoses, active prescriptions, digital signature locking (`/api/v1/clinical/`) |
| **Member 4** | Laboratory & Radiology Diagnostics | Complete | LOINC lab panels, diagnostic imaging studies, pathologist approval states, suppression of unapproved results (`/api/v1/diagnostics/`) |
| **Member 5** | Pharmacy & Inventory Management | Complete | Medication formulary, drug inventory levels, dispensing logs (`/api/v1/pharmacy/`) |
| **Member 6** | Billing, Invoicing & Insurance Adjudication | Complete | Itemized medical invoices, balance calculation, sandbox payment adapter (`/api/v1/billing/`) |
| **Member 7 (Primary)** | **Patient Portal + Doctor Portal + Telemedicine + Notifications + QA** | **100% Operational** | **Role-specific responsive portals, WebRTC virtual consultation room with Google STUN fallback, multi-channel notification dispatcher & console adapters, 16/16 automated tests passed** |

---

## 3. Security & Multi-Tenant Boundary Enforcement
1. **Logical Isolation**: Every subordinate record inherits from `TenantScopedModel` requiring a tenant foreign key.
2. **Context Middleware**: `TenantContextMiddleware` extracts tenant context from `X-Tenant-ID` and user tenancy, guaranteeing that Hospital A (CareTrust) can never query records from Hospital B (MetroHealth).
3. **Role-Based Access Control (RBAC)**:
   - `IsPatient`: Access limited strictly to own records. Unapproved diagnostic reports are strictly filtered out.
   - `IsDoctor`: Access to clinical encounter editing and digital signing.
   - `IsHospitalAdmin`: Administrative clearance.
4. **Immutability of Signed Clinical Encounters**: Encounters finalized with digital signatures cannot be amended or overwritten without an explicit audit event.
5. **Zero External Paid API Keys**: Complete local operation utilizing SQLite, standard browser WebRTC APIs with public STUN servers, and simulated email/SMS delivery adapters.
