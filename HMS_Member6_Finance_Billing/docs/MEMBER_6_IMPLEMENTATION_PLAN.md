# Member 6 — Detailed Implementation Plan & Contract Specifications

**Workstream:** Member 6 — Hospital Billing, Payments, Insurance, Taxes, Accounting & Integrity  
**Architectural Standard:** SaaS Multi-Tenant Healthcare Enterprise  

---

## 1. Database Entity Map (Member 6 Owned Models)

All models inherit from `TenantScopedModel` (`tenant_id`, `created_at`, `updated_at`, `created_by`):

```
BillingEntity (Hospital legal & tax entity: GSTIN, PAN, Address, State Code)
 ├── ServicePrice (Catalogue code, name, department, base_amount, hsn_sac_code, tax_category)
 └── Invoice (invoice_number, patient_ref, encounter_ref, status, total_gross, total_discount, total_tax, total_net, paid_amount, balance_due, due_date)
      ├── InvoiceLine (service_ref, description, quantity, unit_price, discount, tax_rate, net_amount)
      ├── CreditNote (credit_note_number, original_invoice_id, reason, amount, status, approved_by)
      ├── Payment (payment_number, invoice_id, amount, method, status, idempotency_key, reference_no, settled_at)
      │    ├── PaymentAttempt (gateway_ref, payload, response_code, status, attempted_at)
      │    └── Refund (refund_number, payment_id, amount, reason, status, approved_by, processed_at)
      ├── InsuranceClaim (claim_number, payer_ref, policy_number, pre_auth_code, claim_amount, approved_amount, patient_co_pay, status)
      │    ├── ClaimLine (service_line_ref, billed_amount, allowed_amount, denied_reason)
      │    └── DenialLog (denial_code, reason_description, corrective_action, resubmitted_at)
      └── FinancialAuditEvent (event_type, entity_name, entity_id, actor, payload_diff, ip_address)

ChartOfAccount (account_code, account_name, account_type, is_active, balance)
 └── JournalEntry (entry_number, date, description, status: DRAFT/POSTED/REVERSED, source_document_ref)
      └── JournalLine (account_id, debit_amount, credit_amount, description)

FinancialPeriod (period_name, start_date, end_date, is_closed, closed_at, closed_by)
TaxConfiguration (tax_name, rate_percentage, cgst_rate, sgst_rate, igst_rate, state_code, is_default)
ReconciliationRecord (batch_number, statement_date, total_records, matched_records, discrepancy_count, status)
```

---

## 2. API Contract Plan

| Path | Methods | Description | Role Required |
| :--- | :--- | :--- | :--- |
| `/api/v1/billing/entities/` | GET, POST | Legal billing entities & hospital tax registration | Billing Admin |
| `/api/v1/billing/services/` | GET, POST, PUT | Service price catalogue with HSN/SAC codes | Billing Officer |
| `/api/v1/billing/invoices/` | GET, POST, PATCH | Invoices with line items, calculations & status changes | Billing Officer |
| `/api/v1/billing/invoices/{id}/timeline/` | GET | Unified Financial Timeline for an invoice | Finance / Billing |
| `/api/v1/billing/credit-notes/` | GET, POST | Concessions and credit notes | Finance Manager |
| `/api/v1/payments/` | GET, POST | Record payments with idempotency check & receipting | Cashier / Officer |
| `/api/v1/payments/refunds/` | GET, POST, PATCH | Multi-tier refund requests and approvals | Finance Admin |
| `/api/v1/payments/reconciliation/` | GET, POST | Bank/Gateway batch reconciliation | Finance Manager |
| `/api/v1/insurance/payers/` | GET, POST | Insurance companies and TPAs | Insurance Desk |
| `/api/v1/insurance/claims/` | GET, POST, PATCH | Claim preparation, submission & adjudication | Claims Officer |
| `/api/v1/insurance/denial-workbench/` | GET, POST | Denial management, resubmission tracking | Claims Officer |
| `/api/v1/taxes/configurations/` | GET, POST, PUT | GST tax rules, intra/inter-state rates | Finance Admin |
| `/api/v1/taxes/summary/` | GET | GSTR summary report (B2B, B2C, exempt) | Finance Admin |
| `/api/v1/accounting/accounts/` | GET, POST | Chart of Accounts | Chief Accountant |
| `/api/v1/accounting/journals/` | GET, POST | Double-entry journals (strict debit == credit) | Accountant |
| `/api/v1/accounting/ledger/` | GET | General ledger account balance history | Accountant |
| `/api/v1/accounting/receivables/` | GET | AR aging buckets (0-30, 31-60, 61-90, 90+) | Finance Admin |
| `/api/v1/accounting/payables/` | GET, POST | Supplier procurement invoices & payouts | Accountant |
| `/api/v1/accounting/period-closing/` | GET, POST | Period closing verification & lock workflow | Chief Accountant |
| `/api/v1/analytics/dashboard/` | GET | Key KPIs: revenue, collections, AR, claims | All Finance Roles|
| `/api/v1/analytics/integrity-monitor/`| GET | Automated check for unposted/unbalanced items | Chief Accountant |
| `/api/v1/analytics/audit-log/` | GET | Append-only financial audit trails | Auditor / Admin |

---

## 3. Financial Integrity & Security Rules

1. **Zero Floating Point Arithmetic:** All amounts use `Decimal(10, 2)` or `Decimal(12, 4)`. No IEEE 754 float casting.
2. **Double-Entry Equality Invariant:** Every posted journal entry must satisfy:
   $$\sum \text{Debit} - \sum \text{Credit} = 0$$
3. **Strict State Transitions:**
   - Invoices in `PAID` state cannot be edited; adjustments require an authorized `CreditNote`.
   - Invoices in `CANCELLED` state cannot accept payments.
4. **Idempotency Protection:** Payment processing requires an `Idempotency-Key` HTTP header or unique transaction token. Duplicate submissions return the existing receipt without duplicate charges.
5. **Multi-Tenant Isolation:** All queries filter on `tenant_id`. Middleware verifies user tenant membership. Cross-tenant leakage is strictly checked in test suite.
6. **Closed Period Immutability:** Transactions with dates falling inside a closed `FinancialPeriod` cannot be created or modified.
