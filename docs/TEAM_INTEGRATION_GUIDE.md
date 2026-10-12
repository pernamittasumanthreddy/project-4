# Member 4 — Team Integration Developer Handbook
## Laboratory & Radiology Service Consumer Guide

### 1. Header Authentication & Multi-Tenancy
All requests to Member 4's endpoints must specify the tenant identifier header:
```http
X-Tenant-ID: TENANT-001
Authorization: Bearer <JWT_TOKEN_FROM_MEMBER_1>
```

### 2. Member 2 (Patient Registry) Integration
Member 4 uses the standardized `PatientContract`. When creating a lab or imaging order:
- Member 4 verifies patient existence via `PatientContract`.
- If MRN reconciliation is needed, use `PatientIdentityMatcher.match_patient()`.

### 3. Member 3 (EMR Encounters) Integration
Orders can be linked to active clinical encounters:
```json
{
  "encounter_id": "ENC-2026-0042",
  "patient_id": "PT-001",
  "test_panel_id": 1,
  "clinical_notes": "Routine diabetic monitoring"
}
```

### 4. Member 6 (Billing & Finance) Event Consumption
Upon sample accessioning or radiology scan completion, Member 4 emits billable events:
```json
{
  "event_type": "BILLABLE_ITEM_CHARGED",
  "source_module": "LIS",
  "order_id": "ORD-101",
  "cpt_code": "80053",
  "amount_cents": 4500,
  "currency": "USD"
}
```
