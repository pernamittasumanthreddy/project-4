import uuid
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from apps.tenants.models import Tenant, Branch
from apps.taxes.models import TaxConfiguration, TaxTransaction
from apps.billing.models import BillingEntity, ServicePrice, Invoice, InvoiceLine, CreditNote
from apps.payments.models import Payment, Refund, ReconciliationRecord
from apps.insurance.models import InsurancePayer, InsurancePolicy, InsuranceClaim, DenialLog
from apps.accounting.models import ChartOfAccount, JournalEntry, JournalLine, FinancialPeriod, PayableRecord
from apps.analytics.models import FinancialAuditEvent
from apps.common.contracts import MOCK_PATIENTS
from apps.common.decimal_utils import quantize_currency

class Command(BaseCommand):
    help = "Seeds realistic, multi-tenant healthcare financial data for Member 6 modules"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Beginning Member 6 financial master data seeding..."))

        # 1. Tenants & Branches
        tenant_1, _ = Tenant.objects.get_or_create(
            slug="apollo-delhi",
            defaults={
                "id": "tenant-apollo-01",
                "name": "Apollo Super Speciality Hospital",
                "domain": "apollo.delhi.hms.local",
                "subscription_tier": "ENTERPRISE",
                "default_currency": "INR",
                "is_active": True
            }
        )
        branch_1, _ = Branch.objects.get_or_create(
            tenant=tenant_1,
            code="DEL-MAIN",
            defaults={
                "id": "branch-delhi-01",
                "name": "Apollo Delhi Central Hospital",
                "city": "New Delhi",
                "state_code": "07",
                "gstin": "07AAAAA0000A1Z5",
                "address": "Sarita Vihar, Mathura Road, New Delhi 110076",
                "phone": "+91 11 2692 5858",
                "email": "billing@apollo.delhi.hms.local"
            }
        )

        tenant_2, _ = Tenant.objects.get_or_create(
            slug="max-mumbai",
            defaults={
                "id": "tenant-max-02",
                "name": "Max Healthcare Institute",
                "domain": "max.mumbai.hms.local",
                "subscription_tier": "ENTERPRISE",
                "default_currency": "INR",
                "is_active": True
            }
        )
        branch_2, _ = Branch.objects.get_or_create(
            tenant=tenant_2,
            code="MUM-SOUTH",
            defaults={
                "id": "branch-mumbai-01",
                "name": "Max Mumbai South Branch",
                "city": "Mumbai",
                "state_code": "27",
                "gstin": "27BBBBB1111B1Z9",
                "address": "Bandra West, Mumbai 400050",
                "phone": "+91 22 6677 8899",
                "email": "accounts@max.mumbai.hms.local"
            }
        )

        self.stdout.write(self.style.SUCCESS(f"Configured 2 Tenants: '{tenant_1.name}' and '{tenant_2.name}'"))

        # 2. Tax Configurations for Tenant 1
        tax_slabs = [
            ("GST_EXEMPT", "Healthcare Service Exempt", Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), Decimal('0.00'), "999312", True),
            ("GST_5", "Medical Devices / Dialysis 5%", Decimal('5.00'), Decimal('2.50'), Decimal('2.50'), Decimal('5.00'), "999313", False),
            ("GST_12", "Surgical Consumables & Implants 12%", Decimal('12.00'), Decimal('6.00'), Decimal('6.00'), Decimal('12.00'), "901800", False),
            ("GST_18", "Diagnostic Software & Admin Tech 18%", Decimal('18.00'), Decimal('9.00'), Decimal('9.00'), Decimal('18.00'), "998314", False),
        ]
        created_taxes = {}
        for code, name, tot, cgst, sgst, igst, hsn, is_def in tax_slabs:
            t, _ = TaxConfiguration.objects.get_or_create(
                tenant=tenant_1,
                code=code,
                defaults={
                    "name": name,
                    "rate_percentage": tot,
                    "cgst_rate": cgst,
                    "sgst_rate": sgst,
                    "igst_rate": igst,
                    "hsn_sac_code": hsn,
                    "is_default": is_def,
                    "is_active": True
                }
            )
            created_taxes[code] = t

        # 3. Billing Entity for Tenant 1
        billing_entity, _ = BillingEntity.objects.get_or_create(
            tenant=tenant_1,
            gstin="07AAAAA0000A1Z5",
            defaults={
                "branch": branch_1,
                "name": "Apollo Hospitals Delhi Enterprise Ltd",
                "legal_name": "Apollo Hospitals Enterprise Limited (Delhi Unit)",
                "pan": "AAAAA0000A",
                "state_code": "07",
                "state_name": "Delhi",
                "address": "Mathura Road, Sarita Vihar, New Delhi - 110076",
                "contact_phone": "+91 11 2692 5858",
                "contact_email": "finance.delhi@apollohospitals.com",
                "invoice_prefix": "INV-DEL-26",
                "invoice_next_seq": 1001,
                "is_active": True
            }
        )

        # 4. Service Catalogue for Tenant 1
        services = [
            ("SRV-OPD-01", "Senior Consultant OPD Consultation", "OPD", Decimal('1200.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-OPD-02", "Specialist Doctor Follow-up Visit", "OPD", Decimal('600.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-IPD-01", "Deluxe Single Room Bed Charge (Per Day)", "IPD", Decimal('7500.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-IPD-02", "Intensive Care Unit (ICU) Comprehensive Care", "IPD", Decimal('18000.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-LAB-01", "Complete Blood Count (CBC) with Automated Differential", "LAB", Decimal('550.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-LAB-02", "Comprehensive Metabolic Panel (CMP-14)", "LAB", Decimal('1450.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-LAB-03", "HbA1c Glycated Hemoglobin Diagnostic", "LAB", Decimal('700.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-RAD-01", "Digital Chest X-Ray (PA & Lateral Views)", "RAD", Decimal('950.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-RAD-02", "1.5T MRI Brain with Neuro Contrast", "RAD", Decimal('9500.00'), "999312", created_taxes["GST_EXEMPT"]),
            ("SRV-PHARM-01", "IV Meropenem 1g Broad Spectrum Antibiotic", "PHARM", Decimal('2250.00'), "300400", created_taxes["GST_12"]),
            ("SRV-PHARM-02", "IV Paracetamol 1000mg Analgesic Infusion", "PHARM", Decimal('180.00'), "300400", created_taxes["GST_12"]),
            ("SRV-SURG-01", "Laparoscopic Cholecystectomy Surgeon Fee", "SURG", Decimal('55000.00'), "999312", created_taxes["GST_EXEMPT"]),
        ]
        created_services = {}
        for code, name, dept, amt, hsn, tax in services:
            s, _ = ServicePrice.objects.get_or_create(
                tenant=tenant_1,
                code=code,
                defaults={
                    "name": name,
                    "department": dept,
                    "base_amount": amt,
                    "hsn_sac_code": hsn,
                    "tax_config": tax,
                    "is_active": True
                }
            )
            created_services[code] = s

        # 5. Chart of Accounts for Tenant 1
        coa_data = [
            ("1010", "State Bank of India - Current A/c", "ASSET", Decimal('1542000.00')),
            ("1020", "Hospital Cash Counter Petty Till", "ASSET", Decimal('45000.00')),
            ("1100", "Accounts Receivable - Patients & TPAs", "ASSET", Decimal('325000.00')),
            ("2010", "Accounts Payable - Medical Vendors", "LIABILITY", Decimal('140000.00')),
            ("2100", "Output CGST Payable", "LIABILITY", Decimal('14200.00')),
            ("2110", "Output SGST Payable", "LIABILITY", Decimal('14200.00')),
            ("2120", "Output IGST Payable", "LIABILITY", Decimal('6800.00')),
            ("3010", "Hospital Retained Earnings & Capital", "EQUITY", Decimal('1000000.00')),
            ("4010", "OPD Consultation Revenue", "REVENUE", Decimal('245000.00')),
            ("4020", "IPD Room & Nursing Revenue", "REVENUE", Decimal('420000.00')),
            ("4030", "Laboratory Pathology Revenue", "REVENUE", Decimal('185000.00')),
            ("4040", "Radiology Diagnostic Revenue", "REVENUE", Decimal('210000.00')),
            ("4050", "Pharmacy Sales Revenue", "REVENUE", Decimal('135000.00')),
            ("5010", "Medical Consumables & Reagent Expense", "EXPENSE", Decimal('82000.00')),
        ]
        for acct_code, acct_name, acct_type, bal in coa_data:
            ChartOfAccount.objects.get_or_create(
                tenant=tenant_1,
                account_code=acct_code,
                defaults={
                    "account_name": acct_name,
                    "account_type": acct_type,
                    "current_balance": bal,
                    "is_active": True
                }
            )

        # 6. Financial Periods
        FinancialPeriod.objects.get_or_create(
            tenant=tenant_1,
            period_name="FY2026-M09",
            defaults={
                "start_date": timezone.now().date().replace(day=1) - timedelta(days=30),
                "end_date": timezone.now().date().replace(day=1) - timedelta(days=1),
                "is_closed": True,
                "closed_at": timezone.now() - timedelta(days=12),
                "closed_by": "cfo_delhi",
                "closing_notes": "September 2026 financial month audited and closed successfully."
            }
        )
        FinancialPeriod.objects.get_or_create(
            tenant=tenant_1,
            period_name="FY2026-M10",
            defaults={
                "start_date": timezone.now().date().replace(day=1),
                "end_date": timezone.now().date().replace(day=28) + timedelta(days=4),
                "is_closed": False,
                "closing_notes": "Active operational period."
            }
        )

        # 7. Insurance Payers & Policies
        payer_star, _ = InsurancePayer.objects.get_or_create(
            tenant=tenant_1,
            code="STAR-HEALTH",
            defaults={
                "name": "Star Health and Allied Insurance",
                "payer_type": "PRIVATE_INSURER",
                "tpa_contact_email": "claims@starhealth.in",
                "tpa_contact_phone": "+91 44 2828 8800",
                "settlement_tat_days": 10,
                "is_active": True
            }
        )
        payer_hdfc, _ = InsurancePayer.objects.get_or_create(
            tenant=tenant_1,
            code="HDFC-ERGO",
            defaults={
                "name": "HDFC ERGO Health Insurance",
                "payer_type": "PRIVATE_INSURER",
                "tpa_contact_email": "tpa.helpdesk@hdfcergo.com",
                "tpa_contact_phone": "+91 22 6234 6234",
                "settlement_tat_days": 14,
                "is_active": True
            }
        )
        payer_pmjay, _ = InsurancePayer.objects.get_or_create(
            tenant=tenant_1,
            code="AB-PMJAY",
            defaults={
                "name": "Ayushman Bharat PM-JAY Scheme",
                "payer_type": "GOVERNMENT_SCHEME",
                "tpa_contact_email": "portal@pmjay.gov.in",
                "tpa_contact_phone": "14555",
                "settlement_tat_days": 21,
                "is_active": True
            }
        )

        policy_1, _ = InsurancePolicy.objects.get_or_create(
            tenant=tenant_1,
            policy_number="POL-SH-2026-88129",
            defaults={
                "patient_id": "PAT-1001",
                "patient_name": "Aarav Sharma",
                "payer": payer_star,
                "card_number": "SHC-9923841",
                "sum_insured": Decimal('500000.00'),
                "copay_percentage": Decimal('10.00'),
                "valid_from": timezone.now().date() - timedelta(days=180),
                "valid_to": timezone.now().date() + timedelta(days=185),
                "is_active": True
            }
        )

        policy_2, _ = InsurancePolicy.objects.get_or_create(
            tenant=tenant_1,
            policy_number="POL-HDFC-2026-44319",
            defaults={
                "patient_id": "PAT-1002",
                "patient_name": "Priyanka Patel",
                "payer": payer_hdfc,
                "card_number": "HEC-7712399",
                "sum_insured": Decimal('1000000.00'),
                "copay_percentage": Decimal('5.00'),
                "valid_from": timezone.now().date() - timedelta(days=90),
                "valid_to": timezone.now().date() + timedelta(days=275),
                "is_active": True
            }
        )

        # 8. Create Invoices with Lines, Payments, and Claims
        # Invoice 1: Fully Paid OPD Consultation & Lab Test
        inv_1, created_inv_1 = Invoice.objects.get_or_create(
            tenant=tenant_1,
            invoice_number="INV-DEL-26-01001",
            defaults={
                "billing_entity": billing_entity,
                "patient_id": "PAT-1001",
                "patient_name": "Aarav Sharma",
                "patient_mrn": "MRN-2026-00891",
                "patient_state_code": "07",
                "encounter_id": "ENC-5001",
                "encounter_type": "OPD",
                "status": "PAID",
                "issue_date": timezone.now().date() - timedelta(days=3),
                "due_date": timezone.now().date() + timedelta(days=7),
                "notes": "Consultation and blood diagnostic panel."
            }
        )
        if created_inv_1:
            InvoiceLine.objects.create(
                tenant=tenant_1,
                invoice=inv_1,
                service_code=created_services["SRV-OPD-01"].code,
                service_name=created_services["SRV-OPD-01"].name,
                department="OPD",
                quantity=Decimal('1.00'),
                unit_price=created_services["SRV-OPD-01"].base_amount,
                tax_config=created_taxes["GST_EXEMPT"]
            )
            InvoiceLine.objects.create(
                tenant=tenant_1,
                invoice=inv_1,
                service_code=created_services["SRV-LAB-01"].code,
                service_name=created_services["SRV-LAB-01"].name,
                department="LAB",
                quantity=Decimal('1.00'),
                unit_price=created_services["SRV-LAB-01"].base_amount,
                tax_config=created_taxes["GST_EXEMPT"]
            )
            inv_1.recalculate_totals()
            
            # Payment 1
            p1 = Payment.objects.create(
                tenant=tenant_1,
                payment_number="PAY-2026-00101",
                invoice=inv_1,
                amount=inv_1.total_net,
                method="UPI",
                status="SUCCESS",
                idempotency_key="idemp-seed-pay-01",
                transaction_reference="UPI/20261011/998129034",
                received_by="counter_receptionist"
            )
            inv_1.paid_amount = inv_1.total_net
            inv_1.recalculate_totals()

        # Invoice 2: Partially Paid Inpatient Admission
        inv_2, created_inv_2 = Invoice.objects.get_or_create(
            tenant=tenant_1,
            invoice_number="INV-DEL-26-01002",
            defaults={
                "billing_entity": billing_entity,
                "patient_id": "PAT-1002",
                "patient_name": "Priyanka Patel",
                "patient_mrn": "MRN-2026-00912",
                "patient_state_code": "27", # Maharashtra (Inter-state relative to Delhi 07)
                "encounter_id": "ENC-5002",
                "encounter_type": "IPD",
                "status": "PARTIALLY_PAID",
                "issue_date": timezone.now().date() - timedelta(days=2),
                "due_date": timezone.now().date() + timedelta(days=12),
                "notes": "3-day inpatient orthopedic admission."
            }
        )
        if created_inv_2:
            InvoiceLine.objects.create(
                tenant=tenant_1,
                invoice=inv_2,
                service_code=created_services["SRV-IPD-01"].code,
                service_name=created_services["SRV-IPD-01"].name,
                department="IPD",
                quantity=Decimal('3.00'),
                unit_price=created_services["SRV-IPD-01"].base_amount,
                tax_config=created_taxes["GST_EXEMPT"]
            )
            InvoiceLine.objects.create(
                tenant=tenant_1,
                invoice=inv_2,
                service_code=created_services["SRV-RAD-02"].code,
                service_name=created_services["SRV-RAD-02"].name,
                department="RAD",
                quantity=Decimal('1.00'),
                unit_price=created_services["SRV-RAD-02"].base_amount,
                tax_config=created_taxes["GST_EXEMPT"]
            )
            InvoiceLine.objects.create(
                tenant=tenant_1,
                invoice=inv_2,
                service_code=created_services["SRV-PHARM-01"].code,
                service_name=created_services["SRV-PHARM-01"].name,
                department="PHARM",
                quantity=Decimal('2.00'),
                unit_price=created_services["SRV-PHARM-01"].base_amount,
                tax_config=created_taxes["GST_12"] # 12% GST
            )
            inv_2.recalculate_totals()
            
            # Partial advance payment
            p2 = Payment.objects.create(
                tenant=tenant_1,
                payment_number="PAY-2026-00102",
                invoice=inv_2,
                amount=Decimal('15000.00'),
                method="CARD",
                status="SUCCESS",
                idempotency_key="idemp-seed-pay-02",
                transaction_reference="POS-AUTH-908231",
                received_by="ipd_cashier"
            )
            inv_2.paid_amount = Decimal('15000.00')
            inv_2.recalculate_totals()

        # Invoice 3: Under Insurance Claim (Rejected initially -> Placed on Denial Workbench)
        inv_3, created_inv_3 = Invoice.objects.get_or_create(
            tenant=tenant_1,
            invoice_number="INV-DEL-26-01003",
            defaults={
                "billing_entity": billing_entity,
                "patient_id": "PAT-1003",
                "patient_name": "Rohan Deshmukh",
                "patient_mrn": "MRN-2026-01044",
                "patient_state_code": "07",
                "encounter_id": "ENC-5003",
                "encounter_type": "IPD",
                "status": "ISSUED",
                "issue_date": timezone.now().date() - timedelta(days=1),
                "due_date": timezone.now().date() + timedelta(days=14),
                "notes": "Emergency surgical laparoscopy billed under Star Health."
            }
        )
        if created_inv_3:
            InvoiceLine.objects.create(
                tenant=tenant_1,
                invoice=inv_3,
                service_code=created_services["SRV-SURG-01"].code,
                service_name=created_services["SRV-SURG-01"].name,
                department="SURG",
                quantity=Decimal('1.00'),
                unit_price=created_services["SRV-SURG-01"].base_amount,
                tax_config=created_taxes["GST_EXEMPT"]
            )
            inv_3.recalculate_totals()

            # Insurance Claim with Denial Log for the Denial Workbench
            claim_1 = InsuranceClaim.objects.create(
                tenant=tenant_1,
                claim_number="CLM-2026-00088",
                invoice=inv_3,
                payer=payer_star,
                policy=policy_1,
                pre_auth_number="PA-STAR-88120",
                claim_amount=inv_3.total_net,
                approved_amount=Decimal('0.00'),
                patient_copay_amount=Decimal('0.00'),
                status="REJECTED",
                denial_reason="Discharge summary missing treating surgeon operative signature."
            )
            DenialLog.objects.create(
                tenant=tenant_1,
                claim=claim_1,
                denial_code="DOCS_MISSING",
                denial_reason="Discharge summary missing treating surgeon operative signature.",
                resolved=False
            )

        # 9. Smart Reconciliation Batch
        ReconciliationRecord.objects.get_or_create(
            tenant=tenant_1,
            batch_number="RECON-20261011-BAT01",
            defaults={
                "statement_date": timezone.now().date() - timedelta(days=1),
                "total_records": 14,
                "matched_records": 13,
                "discrepancy_count": 1,
                "total_statement_amount": Decimal('148500.00'),
                "total_system_amount": Decimal('149000.00'),
                "status": "DISCREPANCY_DETECTED",
                "notes": "Single settlement discrepancy: ₹500 POS merchant fee deduction unlinked."
            }
        )

        # 10. Accounts Payable Record
        PayableRecord.objects.get_or_create(
            tenant=tenant_1,
            bill_number="BILL-SUP-2026-891",
            defaults={
                "vendor_name": "Medtronic India Surgical Devices",
                "category": "Laparoscopy Trocars & Consumables",
                "due_date": timezone.now().date() + timedelta(days=20),
                "total_amount": Decimal('68000.00'),
                "paid_amount": Decimal('0.00'),
                "balance_due": Decimal('68000.00'),
                "status": "PENDING"
            }
        )

        self.stdout.write(self.style.SUCCESS("Master financial data seeded successfully for Member 6!"))
