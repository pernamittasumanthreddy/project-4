# Repository Audit & Baseline Assessment

**Project:** Hospital Management System (HMS) — Multi-Tenant SaaS Healthcare Platform  
**Audit Scope:** Initial Repository Inspection & Architecture Baseline  
**Auditor:** Senior Software Architect & Lead Engineer (Member 6 — Finance, Billing & Accounting)  
**Date:** October 2026  

---

## 1. Executive Summary

A comprehensive repository inspection was conducted on the HMS workspace (`c:\Users\pedha\OneDrive\Desktop\HMS`). 
The workspace initially contained an uninitialized directory without prior commits, code modules, or configuration files.

Rather than an arbitrary or disconnected build, this assessment establishes the standard architectural foundation for a multi-tenant healthcare enterprise system, while strictly enforcing the role limitation: **Member 6 exclusively implements Billing, Payment Processing, Insurance & Claims, GST & Tax Configuration, Accounting, and Financial Analytics.**

---

## 2. Environment & Toolchain Inspection

| Component | Detected Version | Target / Configuration | Status |
| :--- | :--- | :--- | :--- |
| **Operating System** | Windows 11 / PowerShell | Windows PowerShell execution policy requires `.cmd` wrappers for Node tools | Operational |
| **Python** | 3.13.1 | Python Virtual Environment (`venv`) | Operational |
| **Node.js** | v24.19.0 | Active runtime | Operational |
| **NPM** | 11.17.0 | Via `npm.cmd` / `npx.cmd` | Operational |
| **Git** | 2.55.0.windows.3 | Local repo initialized on `main`; feature branches allocated | Operational |
| **Database** | SQLite (dev/test) / PostgreSQL (prod) | Decimal-safe precision, foreign keys enabled, tenant isolation schema | Configured |
| **Docker** | Not in host PATH | Dockerfile and Docker Compose configurations supplied for deployment | Documented |

---

## 3. Analysis of Existing Assets & Technical Debt

- **Initial State:** Empty repository. No legacy code debt, broken migrations, or conflicting libraries to remediate.
- **Architectural Risk Avoidance:** Because multiple team members contribute across modules, the absence of clean integration boundaries would lead to cross-module coupling. We establish strict contract interfaces (mockable schema definitions for Patients, Encounters, Billable Orders from Labs/Pharmacy/OPD/IPD).
- **Security Baseline:**
  - Enforce server-side multi-tenant scoping on every database query and mutation.
  - Reject untrusted client-supplied tenant IDs without tenant membership validation.
  - Implement zero floating-point arithmetic for monetary calculations (`Decimal` with two or four decimal places).
  - Enforce double-entry bookkeeping validation: unbalanced journal entries ($Debit \neq Credit$) are structurally rejected.
  - Provide idempotency keys on payment operations to prevent accidental double-billing.

---

## 4. Multi-Tenant Strategy

We select a **Shared Database with Enforced Tenant Partitioning** pattern:
- Every tenant-owned table inherits from `TenantScopedModel` with foreign key `tenant_id` and indexing.
- Incoming requests provide tenant context via header (`X-Tenant-ID`) or authenticated user session claims.
- Django queryset filtering automatically scopes records to the active tenant.
- Cross-tenant access is tested and strictly forbidden by 403 Forbidden / 404 Not Found responses.
