# Member 4 — Agile Sprint Backlog & Delivery Records
## Laboratory (LIS) & Radiology (RIS) Module

### Sprint 1: Architecture, Core Schemas & Multi-Tenant Isolation
- **Story M4-S1-01**: Setup multi-tenant database models for LIS & RIS (Panels, Tests, Specimen Containers, Modality Suites).
- **Story M4-S1-02**: Enforce TenantHeaderMiddleware and tenant-isolated ORM querying across all endpoints.
- **Story M4-S1-03**: Integrate contracts for Member 1 (Auth), Member 2 (Patients), Member 3 (Encounters), and Member 6 (Billing).

### Sprint 2: LIS Clinical Workflows, Accessioning & PDF Reports
- **Story M4-S2-01**: Complete test catalog with 1,000+ curated LOINC clinical codes and departmental grouping.
- **Story M4-S2-02**: Implement accessioning barcode generator (ACC-YYYYMMDD-XXXX) and sample tube tracking.
- **Story M4-S2-03**: Two-tier technical entry and pathologist validation with automated panic range flagging.
- **Story M4-S2-04**: Pixel-perfect ReportLab PDF diagnostic reports with demographic headers and flagged results.

### Sprint 3: RIS Imaging Workflows, Modality Worklist & DICOM Engine
- **Story M4-S3-01**: CPT radiology catalog with relative value units, body regions, and preparation instructions.
- **Story M4-S3-02**: Modality Worklist (MWL) management with technician assignments and scan status transitions.
- **Story M4-S3-03**: Synthetic PyDICOM Part 10 generation with accurate patient, series, and SOP Instance UIDs.
- **Story M4-S3-04**: DICOMweb WADO-RS rendered frame endpoint and HTML5 Canvas viewer with interactive calipers.

### Sprint 4: Interoperability, Quality Control & Enterprise Compliance
- **Story M4-S4-01**: Bi-directional HL7 v2.5.1 (ORM/ORU) messaging and FHIR R4 DiagnosticReport / Observation generators.
- **Story M4-S4-02**: CLSI C24-A4 Westgard Multirule engine (1-2s, 1-3s, 2-2s, R-4s, 4-1s, 10-x) and SVG Levey-Jennings charts.
- **Story M4-S4-03**: CLIA/CAP immutable audit trail, HIPAA Safe Harbor PHI sanitizer, and radiation dose monitoring.
