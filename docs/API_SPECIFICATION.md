# HMS Enterprise REST API Specification (v1.7.0)

## Base URL
`/api/v1`

## Headers
- `Content-Type: application/json`
- `X-Tenant-ID: caretrust-health` (Active hospital tenant)
- `X-Impersonate-User: <username>` (Used for demo and local role switching)

---

## 1. Member 1: Core Platform & Tenancy (`/core/`)
- `GET /core/me/` — Retrieves authenticated user profile, active tenant, and persona roles.
- `GET /core/demo-personas/` — Lists pre-seeded personas for the 1-Click Role Switcher.
- `POST /core/switch-role/` — Body: `{"username": "doctor_chen"}`. Switches active demo persona.
- `GET /core/tenants/` — Lists available hospital tenants.
- `GET /core/audit-logs/` — HIPAA/HITECH immutable activity audit logs.

## 2. Member 2: Appointments & Directory (`/appointments/`)
- `GET /appointments/departments/` — Lists clinical departments.
- `GET /appointments/doctors/` — Lists licensed physicians (supports `?department=UUID&telemedicine=true`).
- `GET /appointments/doctors/{id}/available-slots/?date=YYYY-MM-DD` — Real calculated available consultation slots.
- `GET /appointments/` — Lists appointments.
- `POST /appointments/` — Books appointment. Body: `{doctor_id, appointment_date, start_time, appointment_type, reason_for_visit}`.
- `POST /appointments/{id}/cancel/` — Cancels scheduled appointment.

## 3. Member 3: Clinical Encounters & EMR (`/clinical/`)
- `GET /clinical/encounters/` — Lists encounters.
- `POST /clinical/encounters/` — Creates encounter.
- `POST /clinical/encounters/{id}/sign/` — Digitally signs and locks encounter.
- `GET /clinical/prescriptions/` — Lists active and past prescriptions.
- `GET /clinical/patient/{id}/summary/` — Longitudinal EMR record.

## 4. Member 4: Diagnostics (`/diagnostics/`)
- `GET /diagnostics/lab-reports/` — Lists lab reports (patients only receive APPROVED reports).
- `POST /diagnostics/lab-reports/{id}/approve/` — Pathologist approves and publishes report.
- `GET /diagnostics/radiology-reports/` — Lists diagnostic imaging reports.

## 5. Member 5: Pharmacy (`/pharmacy/`)
- `GET /pharmacy/medications/` — Formulary stock search.
- `GET /pharmacy/dispenses/` — Dispensing history.

## 6. Member 6: Billing (`/billing/`)
- `GET /billing/invoices/` — Itemized invoices.
- `POST /billing/invoices/{id}/pay-sandbox/` — Settles invoice balance via sandbox payment adapter.

## 7. Member 7: Patient Portal (`/patient-portal/`)
- `GET /patient-portal/dashboard/` — Aggregated dashboard with upcoming visits, active prescriptions, lab results, and billing balance.
- `GET /patient-portal/profile/` — Demographics and emergency contact details.
- `PUT /patient-portal/profile/` — Updates permissible patient contact details (locks clinical diagnoses).
- `GET /patient-portal/medical-records/` — Aggregated EMR record.
- `GET /patient-portal/billing/` — Invoices, balances, and receipts.

## 8. Member 7: Doctor Portal (`/doctor-portal/`)
- `GET /doctor-portal/dashboard/` — Today's clinical schedule, waiting queue, metrics.
- `GET /doctor-portal/schedule/?view=day|week&date=YYYY-MM-DD` — Daily and weekly agenda.
- `GET /doctor-portal/consultation/{appointment_id}/` — Consultation workstation.
- `POST /doctor-portal/consultation/{appointment_id}/` — Saves SOAP notes, vitals, diagnoses, and prescriptions.

## 9. Member 7: Telemedicine (`/telemedicine/`)
- `GET /telemedicine/ice-config/` — Returns STUN server parameters.
- `GET /telemedicine/appointment/{appointment_id}/` — Retrieves virtual room.
- `POST /telemedicine/sessions/{id}/join/` — Body: `{"role": "DOCTOR"|"PATIENT"}`.
- `GET /telemedicine/sessions/{id}/signaling/?role=DOCTOR|PATIENT` — Polls undelivered SDP/ICE messages.
- `POST /telemedicine/sessions/{id}/signaling/` — Posts SDP offer/answer or ICE candidate.
- `POST /telemedicine/sessions/{id}/leave/` — Concludes call session.

## 10. Member 7: Notifications (`/notifications/`)
- `GET /notifications/` — In-app notification inbox.
- `GET /notifications/unread-count/` — Unread count badge.
- `POST /notifications/{id}/read/` — Marks notification as read.
- `POST /notifications/mark-all-read/` — Marks all as read.
- `GET /notifications/delivery-logs/` — Simulated Email & SMS delivery logs.
