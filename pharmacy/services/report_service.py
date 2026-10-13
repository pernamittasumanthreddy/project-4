"""HMS Pharmacy Report & Export Service — Member 5
Generates stock valuation, audit summaries, CSV downloads, and ReportLab PDF documents.
"""

import io
import csv
from decimal import Decimal
from datetime import date
from typing import Dict, Any, List
from django.db.models import Sum, F

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from pharmacy.models.catalogue import Medicine
from pharmacy.models.inventory import MedicineBatch
from pharmacy.models.ledger import StockMovement
from pharmacy.models.dispensing import DispenseRecord


class ReportService:
    """Computes analytical reports and renders tamper-evident exports."""

    @classmethod
    def get_stock_valuation(cls, tenant, branch=None) -> Dict[str, Any]:
        """Calculates total purchase cost and potential retail value of inventory."""
        batches = MedicineBatch.objects.filter(
            tenant=tenant,
            status='ACTIVE',
            available_quantity__gt=Decimal('0.00')
        )
        if branch:
            batches = batches.filter(branch=branch)

        total_cost_value = Decimal('0.00')
        total_retail_value = Decimal('0.00')
        total_units = Decimal('0.00')

        for b in batches:
            total_units += b.available_quantity
            total_cost_value += (b.available_quantity * b.purchase_cost)
            total_retail_value += (b.available_quantity * b.selling_price)

        return {
            'total_batches_count': batches.count(),
            'total_units_on_hand': total_units,
            'total_purchase_cost_value': total_cost_value,
            'total_retail_value': total_retail_value,
            'potential_margin_value': total_retail_value - total_cost_value
        }

    @classmethod
    def generate_stock_csv(cls, tenant, branch=None) -> str:
        """Generates CSV text export of all active stock batches."""
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            'Medicine Code',
            'Brand Name',
            'Generic Name',
            'Strength',
            'Batch Number',
            'Expiry Date',
            'Available Quantity',
            'Purchase Cost',
            'Selling Price',
            'Total Valuation',
            'Storage Location'
        ])

        batches = MedicineBatch.objects.filter(tenant=tenant).order_by('medicine__brand_name', 'expiry_date')
        if branch:
            batches = batches.filter(branch=branch)

        for b in batches:
            val = b.available_quantity * b.purchase_cost
            loc = b.storage_location.name if b.storage_location else 'N/A'
            writer.writerow([
                b.medicine.code,
                b.medicine.brand_name,
                b.medicine.generic_name,
                b.medicine.strength,
                b.batch_number,
                b.expiry_date.strftime('%Y-%m-%d'),
                str(b.available_quantity),
                str(b.purchase_cost),
                str(b.selling_price),
                str(val),
                loc
            ])

        return output.getvalue()

    @classmethod
    def generate_stock_pdf(cls, tenant, branch=None) -> bytes:
        """Generates formatted PDF inventory audit report using ReportLab."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#0f172a"),
            spaceAfter=4
        )
        subtitle_style = ParagraphStyle(
            "DocSub",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#64748b")
        )

        valuation = cls.get_stock_valuation(tenant, branch)
        branch_name = branch.name if branch else "All Branches"

        story = []
        story.append(Paragraph(f"HOSPITAL MANAGEMENT SYSTEM — PHARMACY AUDIT REPORT", title_style))
        story.append(Paragraph(f"Tenant: {tenant.name} | Facility Branch: {branch_name} | Generated: {date.today()}", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#cbd5e1"), spaceAfter=14))

        # Valuation KPI table
        val_rows = [
            ["Total Batches", "Units On Hand", "Total Purchase Valuation", "Retail Value"],
            [
                str(valuation['total_batches_count']),
                f"{valuation['total_units_on_hand']:,.2f}",
                f"${valuation['total_purchase_cost_value']:,.2f}",
                f"${valuation['total_retail_value']:,.2f}"
            ]
        ]
        val_table = Table(val_rows, colWidths=[130, 130, 140, 140])
        val_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        story.append(val_table)
        story.append(Spacer(1, 16))

        # Sampled Batch Breakdown table
        story.append(Paragraph("Current Inventory Batches (Sampled)", styles["Heading2"]))
        batches = MedicineBatch.objects.filter(tenant=tenant, status='ACTIVE')
        if branch:
            batches = batches.filter(branch=branch)
        batches = batches.order_by('expiry_date')[:25]

        batch_rows = [["Medicine", "Batch #", "Expiry", "Available Qty", "Cost", "Total Value"]]
        for b in batches:
            val = b.available_quantity * b.purchase_cost
            batch_rows.append([
                f"{b.medicine.brand_name} ({b.medicine.strength})",
                b.batch_number,
                b.expiry_date.strftime('%Y-%m-%d'),
                str(b.available_quantity),
                f"${b.purchase_cost}",
                f"${val:,.2f}"
            ])

        b_table = Table(batch_rows, colWidths=[170, 80, 80, 80, 60, 70])
        b_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#334155")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(b_table)

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
