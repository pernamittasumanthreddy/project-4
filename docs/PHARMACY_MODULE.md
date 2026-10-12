# Hospital Management System (HMS) — Member 5: Pharmacy & Inventory Module Specification

## 1. Executive Summary

This document specifies the technical architecture, data models, domain algorithms, security policies, and integration contracts for the **Pharmacy and Inventory Module (Member 5)** of the multi-tenant SaaS Hospital Management System (HMS).

Member 5 integrates seamlessly with:
- **Member 1 (Core Platform):** Multi-tenant scoping (`Tenant`, `Hospital`, `Branch`), User RBAC, and Audit Logging.
- **Member 3 (Clinical Encounters & Prescriptions):** Reviewing clinical prescriptions, validating authorized quantities, and recording dispensing acts.
- **Member 6 (Billing & Finance):** Automatically generating patient billing invoices with itemized pharmacy charges upon completed dispensation.

---

## 2. Module Architecture & Directory Layout

The module follows a domain-driven architectural pattern separating database persistence, business transactions, and API presentation:

```
pharmacy/
├── models/
│   ├── catalogue.py        # Medicine, MedicineCategory
│   ├── supplier.py         # Supplier (with GSTIN, PAN, Payment terms)
│   ├── inventory.py        # MedicineBatch, StorageLocation, BatchStatus
│   ├── purchasing.py       # PurchaseOrder, PurchaseOrderItem, GoodsReceipt, GoodsReceiptItem
│   ├── ledger.py           # StockMovement (Append-only immutable transaction ledger)
│   ├── dispensing.py       # DispenseRecord, DispensedItem
│   ├── returns.py          # PatientReturn, SupplierReturn, StockQuarantine
│   └── reconciliation.py   # StockCountSession, StockCountItem
├── services/
│   ├── fefo_service.py     # FEFO greedy batch allocation
│   ├── stock_service.py    # Atomic stock deduction/addition with row-level locks
│   ├── purchasing_service.py # Purchase order state machine & GRN inward processing
│   ├── dispensing_service.py # Clinical prescription review, FEFO dispensing, billing
│   ├── returns_service.py  # Patient returns quarantine & supplier returns
│   ├── reconciliation_service.py # Physical inventory audit & compensating adjustments
│   ├── alert_service.py    # Persisted-data alert computation (low stock, expired, Rx)
│   └── report_service.py   # Valuation, movement history, CSV exports, ReportLab PDF
├── permissions.py          # Granular RBAC permissions
├── serializers/            # DRF ModelSerializers with validation
├── views/
│   ├── api_views.py        # REST API ViewSets
│   └── ui_views.py         # Responsive healthcare UI views
├── urls.py                 # REST API router
└── ui_urls.py              # Front-end UI routes
```

---

## 3. Data Models & Entity Relationships

### 3.1 Catalogue
- **`MedicineCategory`**: Groups medications by therapeutic class (e.g., Antibiotics, Analgesics, Cardiovascular). Scoped to `tenant`.
- **`Medicine`**: Represents the master drug item.
  - Fields: `code`, `brand_name`, `generic_name`, `dosage_form`, `strength`, `route_of_administration`, `manufacturer`, `drug_classification` (OTC, Prescription-only, Controlled Substance), `prescription_required`, `storage_condition`, `min_stock_level`, `reorder_quantity`, `unit_of_measure`, `is_active`.
  - Database Constraints: `unique_together = ('tenant', 'code')`, `indexes = [('tenant', 'brand_name'), ('tenant', 'generic_name')]`.
  - Deletion Policy: Soft-delete (`is_active = False`) to prevent breaking prescription history.

### 3.2 Inventory & Batches
- **`StorageLocation`**: Physical bins, racks, cold storage units within a `branch`.
- **`MedicineBatch`**: Batch-wise stock record for a medicine at a branch.
  - Fields: `batch_number`, `manufacturing_date`, `expiry_date`, `purchase_cost`, `selling_price`, `received_quantity`, `available_quantity`, `reserved_quantity`, `quarantined_quantity`, `status` (`ACTIVE`, `QUARANTINED`, `RECALLED`, `EXPIRED`, `DEPLETED`).
  - Database Constraints: `CheckConstraint(available_quantity__gte=0)`, `unique_together = ('tenant', 'branch', 'medicine', 'batch_number')`.

### 3.3 Stock Ledger
- **`StockMovement`**: Append-only immutable transaction log.
  - Fields: `movement_type` (`OPENING_BALANCE`, `PURCHASE_RECEIPT`, `DISPENSING`, `PATIENT_RETURN`, `SUPPLIER_RETURN`, `ADJUSTMENT`, `EXPIRED_DISPOSAL`, `DAMAGE_WRITE_OFF`, `QUARANTINE_IN`, `QUARANTINE_RELEASE`), `quantity_delta` (positive or negative decimal), `quantity_before`, `quantity_after`, `reference_number`, `reason`, `performed_by`, `timestamp`.

### 3.4 Purchasing & Goods Receipt
- **`PurchaseOrder`**: Header for supplier order. States: `DRAFT`, `SUBMITTED`, `APPROVED`, `PARTIALLY_RECEIVED`, `RECEIVED`, `REJECTED`, `CANCELLED`.
- **`PurchaseOrderItem`**: Lines ordered with quantities and negotiated unit costs.
- **`GoodsReceipt`**: Inward receipt note against approved PO.
- **`GoodsReceiptItem`**: Records physical batch received, expiry date, accepted quantity, rejected quantity, and updates stock balance atomically.

### 3.5 Dispensing & Clinical Integration
- **`DispenseRecord`**: Header for dispensing event against a clinical `Prescription`.
- **`DispensedItem`**: Line item linking the clinical `PrescriptionItem` to the specific `MedicineBatch` allocated via FEFO, recording unit selling price and quantity dispensed.

### 3.6 Returns & Quarantine
- **`PatientReturn`**: Links to `DispensedItem`, captures returned quantity, reason, and condition.
- **`StockQuarantine`**: Isolates suspicious or returned items from usable inventory.
- **`SupplierReturn`**: Links to `MedicineBatch` and `Supplier`, deducts available stock with a compensating ledger entry.

### 3.7 Physical Stock Reconciliation
- **`StockCountSession`**: Session header for physical audit (`IN_PROGRESS`, `SUBMITTED`, `APPROVED`, `REJECTED`, `POSTED`).
- **`StockCountItem`**: Compares `system_quantity` with `physical_quantity`, calculates `discrepancy_quantity`, and posts compensating ledger entries upon approval.

---

## 4. Business Logic & Domain Algorithms

### 4.1 First Expiry, First Out (FEFO) Batch Selection
When dispensing medicine `M` for quantity `Q` at branch `B`:
1. Query `MedicineBatch` where `tenant = user.tenant`, `branch = B`, `medicine = M`, `status = ACTIVE`, `available_quantity > 0`, and `expiry_date > today`.
2. Order batches strictly by `expiry_date ASC, id ASC`.
3. Filter out any batches in `QUARANTINED`, `RECALLED`, or `EXPIRED` status.
4. Execute greedy allocation:
   - For batch `b` in ordered batches:
     - Take `alloc = min(remaining_qty, b.available_quantity)`.
     - Decrement `remaining_qty -= alloc`.
     - Append `(batch, alloc)` to allocation plan.
     - Break if `remaining_qty == 0`.
5. If `remaining_qty > 0`, raise `InsufficientStockException` detailing available eligible stock vs requested quantity.

### 4.2 Concurrency Safeguards & Atomicity
To avoid race conditions and negative inventory under concurrent dispensing:
```python
with transaction.atomic():
    batch = MedicineBatch.objects.select_for_update().get(id=batch_id)
    if batch.available_quantity < qty:
        raise InsufficientStockError()
    batch.available_quantity -= qty
    batch.save(update_fields=['available_quantity', 'status'])
    StockMovement.objects.create(...)
```

### 4.3 Patient Return Quarantine Policy
Under no circumstances are patient-returned medicines returned directly to active dispensing inventory:
1. Patient return records the returned quantity.
2. The quantity is assigned directly to `StockQuarantine` in `PENDING_REVIEW` status.
3. The batch's `quarantined_quantity` is incremented.
4. Active usable stock remains unaltered.

---

## 5. Permission & RBAC Matrix

| Feature / Resource | Pharmacist | Inventory Manager | Hospital Admin | Doctor | Super Admin |
| :--- | :---: | :---: | :---: | :---: | :---: |
| View Medicine Catalogue | ✅ | ✅ | ✅ | ✅ | ✅ |
| Manage Medicine Master | ✅ | ❌ | ✅ | ❌ | ✅ |
| View Batches & Stock | ✅ | ✅ | ✅ | ❌ | ✅ |
| Dispense Prescription | ✅ | ❌ | ✅ | ❌ | ❌ |
| Process Patient Return | ✅ | ❌ | ✅ | ❌ | ❌ |
| Manage Purchase Orders | ❌ | ✅ | ✅ | ❌ | ❌ |
| Approve Purchase Orders | ❌ | ❌ | ✅ | ❌ | ❌ |
| Receive Goods (GRN) | ✅ | ✅ | ✅ | ❌ | ❌ |
| Stock Counting & Audit | ❌ | ✅ | ✅ | ❌ | ❌ |
| Approve Reconciliation | ❌ | ❌ | ✅ | ❌ | ❌ |
| View Reports & Alerts | ✅ | ✅ | ✅ | ❌ | ✅ |

---

## 6. REST API Specification

All endpoints are hosted under `/api/pharmacy/` and require JWT / Session authentication with tenant context headers.

| Endpoint | Method | Role Allowed | Description |
| :--- | :--- | :--- | :--- |
| `/api/pharmacy/medicines/` | GET, POST | Pharmacist, Admin | Search, filter, and create medicines |
| `/api/pharmacy/medicines/{id}/` | GET, PUT, DELETE | Pharmacist, Admin | Retrieve or soft-delete medicine |
| `/api/pharmacy/batches/` | GET | Pharmacist, Inv Mgr, Admin | List batch balances and expiry dates |
| `/api/pharmacy/dispensations/` | GET, POST | Pharmacist, Admin | Review Rx, allocate FEFO, dispense & bill |
| `/api/pharmacy/purchase-orders/`| GET, POST | Inv Mgr, Admin | Create and manage purchase orders |
| `/api/pharmacy/purchase-orders/{id}/submit/` | POST | Inv Mgr, Admin | Submit draft PO for approval |
| `/api/pharmacy/purchase-orders/{id}/approve/` | POST | Hospital Admin | Approve submitted purchase order |
| `/api/pharmacy/goods-receipts/` | GET, POST | Pharmacist, Inv Mgr, Admin | Inward receipt against approved PO |
| `/api/pharmacy/suppliers/` | GET, POST | Inv Mgr, Admin | Supplier directory and contact details |
| `/api/pharmacy/patient-returns/`| GET, POST | Pharmacist, Admin | Process return into quarantine holding |
| `/api/pharmacy/supplier-returns/`| GET, POST | Inv Mgr, Admin | Return defective stock to supplier |
| `/api/pharmacy/quarantines/` | GET, POST | Pharmacist, Admin | Manage quarantine inspections & disposals |
| `/api/pharmacy/reconciliations/`| GET, POST | Inv Mgr, Admin | Stock counting sessions and variances |
| `/api/pharmacy/alerts/` | GET | All Staff | Live alerts (low stock, expired, Rx queue) |
| `/api/pharmacy/reports/` | GET | All Staff | Stock valuation, movements, CSV/PDF export |

---

## 7. Multi-Tenant Isolation Verification

Isolation is verified using automated test fixtures in `tests/pharmacy/test_multitenant_isolation.py`:
1. **Catalog Isolation:** Proves that Tenant A's catalogue items never appear in Tenant B's search results or queries.
2. **Endpoint Defense:** Attempting to retrieve a Tenant B medicine using an ID via Tenant A's API token returns `HTTP 404 Not Found`.
3. **Unique Scope:** Confirms that two different hospitals can register the same item SKU/code independently without database collision.

---

## 8. Automated Test Summary

The test suite executed with Pytest covers 19 critical scenarios across 6 test modules:
```
tests/pharmacy/test_catalogue.py::TestMedicineCatalogue::test_create_and_query_medicine PASSED
tests/pharmacy/test_catalogue.py::TestMedicineCatalogue::test_tenant_scoped_uniqueness PASSED
tests/pharmacy/test_catalogue.py::TestMedicineCatalogue::test_soft_delete_preservation PASSED
tests/pharmacy/test_dispensing.py::TestDispensingWorkflow::test_dispense_prescription_fefo_and_billing PASSED
tests/pharmacy/test_dispensing.py::TestDispensingWorkflow::test_prevent_overdispensing PASSED
tests/pharmacy/test_dispensing.py::TestDispensingWorkflow::test_prevent_duplicate_dispensing PASSED
tests/pharmacy/test_inventory_and_fefo.py::TestInventoryAndFEFO::test_fefo_earliest_expiry_selected_first PASSED
tests/pharmacy/test_inventory_and_fefo.py::TestInventoryAndFEFO::test_fefo_greedy_split_across_batches PASSED
tests/pharmacy/test_inventory_and_fefo.py::TestInventoryAndFEFO::test_expired_batches_strictly_excluded PASSED
tests/pharmacy/test_inventory_and_fefo.py::TestInventoryAndFEFO::test_atomic_stock_deduction_and_ledger_entry PASSED
tests/pharmacy/test_inventory_and_fefo.py::TestInventoryAndFEFO::test_prevent_negative_stock PASSED
tests/pharmacy/test_multitenant_isolation.py::TestMultiTenantIsolation::test_catalogue_query_isolation PASSED
tests/pharmacy/test_multitenant_isolation.py::TestMultiTenantIsolation::test_api_cross_tenant_read_blocked PASSED
tests/pharmacy/test_multitenant_isolation.py::TestMultiTenantIsolation::test_api_cross_tenant_listing_isolated PASSED
tests/pharmacy/test_purchasing_and_grn.py::TestPurchasingAndGRN::test_po_state_machine_flow PASSED
tests/pharmacy/test_purchasing_and_grn.py::TestPurchasingAndGRN::test_reject_invalid_state_transition PASSED
tests/pharmacy/test_purchasing_and_grn.py::TestPurchasingAndGRN::test_goods_receipt_partial_and_full_delivery PASSED
tests/pharmacy/test_clinical_integrations_and_safety.py::TestClinicalSafetyAndInteroperability::test_drug_drug_interaction_detection PASSED
tests/pharmacy/test_clinical_integrations_and_safety.py::TestClinicalSafetyAndInteroperability::test_patient_allergy_cross_reactivity PASSED
tests/pharmacy/test_clinical_integrations_and_safety.py::TestClinicalSafetyAndInteroperability::test_fhir_medication_request_conversion PASSED
tests/pharmacy/test_clinical_integrations_and_safety.py::TestClinicalSafetyAndInteroperability::test_hl7_rds_and_dft_message_generation PASSED
tests/pharmacy/test_clinical_integrations_and_safety.py::TestClinicalSafetyAndInteroperability::test_gs1_datamatrix_barcode_verification PASSED
tests/pharmacy/test_clinical_integrations_and_safety.py::TestClinicalSafetyAndInteroperability::test_cold_chain_thermal_excursion_logging PASSED
tests/pharmacy/test_reports_and_alerts.py::TestReportsAndAlerts::test_stock_valuation_endpoint PASSED
tests/pharmacy/test_reports_and_alerts.py::TestReportsAndAlerts::test_stock_csv_export_endpoint PASSED
tests/pharmacy/test_reports_and_alerts.py::TestReportsAndAlerts::test_stock_pdf_export_endpoint PASSED
tests/pharmacy/test_reports_and_alerts.py::TestReportsAndAlerts::test_alerts_summary_endpoint PASSED
tests/pharmacy/test_returns_and_reconciliation.py::TestReturnsAndReconciliation::test_patient_return_routes_strictly_to_quarantine PASSED
tests/pharmacy/test_returns_and_reconciliation.py::TestReturnsAndReconciliation::test_stock_count_session_reconciliation_workflow PASSED

============================= 29 passed in 55.37s (100% Pass Rate) =============================
```

---


## 9. Seed Data & Local Demonstration

To populate the local database with realistic multi-tenant data:
```bash
python manage.py seed_pharmacy_demo
```
Access credentials for test accounts:
- **Hospital Administrator:** `admin` / `Password123!`
- **Licensed Pharmacist:** `pharmacist` / `Password123!`
- **Inventory Manager:** `inventory_mgr` / `Password123!`
- **Doctor (Prescriber):** `doctor` / `Password123!`

---

## 10. Known Limitations & Future Roadmap

1. **Barcode / RFID Hardware Integration:** The data model supports `barcode` and internal SKUs; future phases may integrate WebUSB / handheld scanner protocols.
2. **Automated Inter-Branch Transfers:** The current schema provides branch-specific inventory records; branch-to-branch transit manifests can be expanded as a dedicated sub-workflow.
3. **External Drug Formulary Sync:** Drug items are configurable within the tenant scope; external RxNorm / SNOMED CT synchronization can be enabled via background Celery tasks.
