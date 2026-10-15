# HMS SaaS — Member 4 Integration Contracts Specification
## Module: Laboratory Information System (LIS) & Radiology Information System (RIS)

### 1. Architectural Scope & Team Responsibility Matrix

| Team Member | Domain | Contract Relationship with Member 4 | Integration Mechanism |
| :--- | :--- | :--- | :--- |
| **Member 1** | Core Platform, Auth, SaaS Multi-Tenancy & RBAC | Provides tenant isolation (`Tenant`, `HospitalBranch`) and user credentials (`UserProfile`, `UserRole`). | HTTP Headers: `X-Tenant-Code`, `X-Tenant-ID`, `X-Branch-ID`, `X-User-Role`. Middleware enforces queryset filters on all models. |
| **Member 2** | Patient Registry & Appointments | Provides master patient demographic references (`PatientContract`: UHID, Name, DOB, Gender, Blood Group). | Foreign key references and synced REST contract endpoints `/api/contracts/patients/`. |
| **Member 3** | EMR / EHR Clinical Encounters | Emits clinician investigation orders linked to outpatient/inpatient encounters (`ClinicalEncounterContract`). | Ingested via `/api/laboratory/orders/` and `/api/radiology/orders/` referencing `encounter_id`. |
| **Member 4** | **Laboratory & Radiology (LIS & RIS)** | **Owner**: Manages test catalogues, order lifecycle, specimen tracking, barcodes, result entry, pathologist/radiologist review, ReportLab PDF generation, DICOMweb PACS endpoints & medical image viewer. | Core implementation within `backend/lis/` and `backend/ris/`. |
| **Member 5** | Pharmacy & Inventory | Reagent and consumable supply requests (e.g., EDTA tubes, contrast media, stain kits). | Standardized reagent catalogue references. |
| **Member 6** | Billing, Insurance & Charge Master | Receives billable investigation events when results/reports are approved. | Emitted via `BillingEventContract` at `/api/contracts/billing-events/`. |
| **Member 7** | Frontend Integration, CI/CD & QA | Ingests OpenAPI 3.0 schema and runs automated integration test suites. | OpenAPI specification at `/api/schema/` and Swagger UI at `/api/docs/`. |

---

### 2. Multi-Tenant Headers Contract (Member 1 $\leftrightarrow$ Member 4)

Every incoming HTTP request must include tenant identification headers. The `TenantHeaderMiddleware` enforces that Hospital A cannot see or mutate Hospital B's clinical orders, specimens, or reports:

```http
GET /api/laboratory/dashboard/ HTTP/1.1
Host: api.hms-saas.com
X-Tenant-Code: metro-general
X-Branch-ID: b3e51a2d-45ab-41d8-82e1-4c7fa43bb180
X-User-Role: LAB_TECHNICIAN
```

---

### 3. Patient Reference Contract (Member 2 $\leftrightarrow$ Member 4)

When Member 4 creates an investigation order or registers a specimen, it references Member 2's master patient record:

```json
{
  "id": "c1f71a9e-56e2-4bf1-a832-7bb8c312a001",
  "uhid": "UHID-2026-00101",
  "first_name": "Eleanor",
  "last_name": "Pemberton",
  "dob": "1968-04-15",
  "gender": "F",
  "blood_group": "A+",
  "phone": "+1 555-0101",
  "allergies": "Penicillin (Moderate)"
}
```

---

### 4. Clinical Order Ingestion Contract (Member 3 $\leftrightarrow$ Member 4)

Clinical encounters in Member 3's EMR module trigger laboratory or radiology orders via:

#### Endpoint: `POST /api/laboratory/orders/`
```json
{
  "patient_id": "c1f71a9e-56e2-4bf1-a832-7bb8c312a001",
  "encounter_id": "ENC-METRO-901",
  "ordering_clinician": "Dr. Elena Rostova, MD",
  "priority": "STAT",
  "clinical_indications": "Acute substernal chest pain radiating to left jaw. Rule out MI.",
  "fasting_status": "Non-fasting",
  "test_ids": [
    "e2f91a9e-56e2-4bf1-a832-7bb8c312b001"
  ]
}
```

**Response (HTTP 201 Created):**
```json
{
  "id": "fa1b9e2a-1122-3344-5566-778899aabbcc",
  "order_number": "ORD-LAB-20261012-7F8A12",
  "accession_number": "ACC-261012-9A4B1",
  "priority": "STAT",
  "status": "SAMPLE_PENDING",
  "specimens": [
    {
      "barcode_id": "SPC-261012-C89E11",
      "specimen_type": "PLASMA",
      "container_type": "Green Heparin Tube",
      "status": "PENDING"
    }
  ]
}
```

---

### 5. Chargeable Event Contract (Member 4 $\rightarrow$ Member 6)

Upon pathologist or radiologist sign-off (`APPROVED` status), Member 4 automatically emits a chargeable billing event:

#### Model: `BillingEventContract`
```json
{
  "id": "89ab12cd-ef34-5678-9012-3456789abcde",
  "module": "LIS",
  "order_id": "ORD-LAB-20261012-STAT01",
  "service_code": "TROP-I",
  "service_name": "High-Sensitivity Troponin I (hs-cTnI)",
  "amount": "55.00",
  "status": "EMITTED",
  "emitted_at": "2026-10-12T07:10:00Z"
}
```

---

### 6. DICOMweb Standard PACS Contract (Member 4 RIS)

Member 4 exposes standard PS3.18 DICOM Web Services:

1. **QIDO-RS (Query Studies)**:
   - `GET /api/dicomweb/studies/`
   - Returns standard DICOM JSON tag dictionary containing `(0020,000D)` Study Instance UID, `(0010,0020)` Patient ID, etc.
2. **WADO-RS (Retrieve Metadata)**:
   - `GET /api/dicomweb/studies/{studyUID}/metadata`
3. **WADO-RS (Retrieve Rendered Frame)**:
   - `GET /api/dicomweb/studies/{studyUID}/series/{seriesUID}/instances/{instanceUID}/rendered`
   - Content-Type: `image/png`
4. **WADO-RS (Retrieve Native DICOM File)**:
   - `GET /api/dicomweb/studies/{studyUID}/series/{seriesUID}/instances/{instanceUID}`
   - Content-Type: `application/dicom`
