# Pull Request #01: Initialize Enterprise Multi-Tenant HMS Foundation & Member 1 Architecture

## Summary
Establishes the core multi-tenant architecture for the Hospital Management System (HMS), including Django 6 settings, custom user model, and tenant data structures.

## Scope of Changes
- `backend/manage.py`: Django entrypoint.
- `backend/hms_core/settings.py`: Multi-tenant settings, CORS configuration, SQLite/PostgreSQL compatibility, zero-key configuration.
- `backend/hms_core/urls.py`: Root routing for all 7 platform member modules.
- `backend/apps/core/models.py`: `Tenant`, `HospitalBranch`, `User`, `TenantScopedModel`, and `AuditLog`.

## Verification Evidence
- Clean Django startup verified with zero deprecation warnings.
- Custom User model with 8 distinct healthcare roles configured.
