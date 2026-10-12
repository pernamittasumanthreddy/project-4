# Contributing Guidelines — Member 6 Pod

Thank you for contributing to the Hospital Management System (HMS) Member 6 finance and billing workstream.

---

## 1. Scope Boundary Rules

1. **Member 6 Only:** All code, models, serializers, endpoints, and frontend views in this repository workstream must belong exclusively to Billing, Payments, Insurance, Taxes, Accounting, and Financial Integrity.
2. **Respect External Contracts:** Do not implement patient registration, clinical encounter workflows, lab analyzers, or pharmacy inventory. Use mock contract adapters or documented external references for those domains.

---

## 2. Financial Engineering Principles

1. **Never Use Binary Floating Point for Money:**
   - Always use Python's `Decimal` type.
   - Always use `models.DecimalField(max_digits=12, decimal_places=2)`.
   - Never use JavaScript native floats without rounding wrappers (`Number.toFixed(2)` or BigNumber).
2. **Double-Entry Balancing Rule:**
   - Every journal entry submitted to the GL must balance. Total debit must equal total credit.
3. **Idempotency on Write Operations:**
   - Every payment mutation must accept an idempotency token to protect against network timeouts and duplicate browser submissions.
4. **Tenant Isolation:**
   - Every database query must be tenant-aware.
   - Never trust an unverified client tenant header.

---

## 3. Git Branching & Commits

- Work on feature branch: `feature/member-6-finance-billing`
- Commit format:
  - `feat(billing): ...`
  - `feat(payments): ...`
  - `feat(insurance): ...`
  - `feat(accounting): ...`
  - `test(finance): ...`
