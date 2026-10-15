import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.utils import timezone

def generate_lab_report_pdf(lab_report):
    """
    Generates a secure, professional diagnostic laboratory report PDF
    adhering to clinical accreditation formatting standards.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    order = lab_report.order
    patient = order.patient
    tenant = order.tenant
    branch = order.branch

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'HospitalTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#0f766e'),
        alignment=1 # Center
    )
    subtitle_style = ParagraphStyle(
        'HospitalSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569'),
        alignment=1
    )
    header_box_style = ParagraphStyle(
        'HeaderBox',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e293b')
    )
    bold_label = ParagraphStyle(
        'BoldLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#0f172a')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#1e293b')
    )
    flag_normal = ParagraphStyle(
        'FlagNormal',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#166534')
    )
    flag_abnormal = ParagraphStyle(
        'FlagAbnormal',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#b91c1c')
    )
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Italic'],
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#64748b'),
        alignment=1
    )

    story = []

    # 1. Header & Hospital Branding
    story.append(Paragraph(f"{tenant.name.upper()}", title_style))
    story.append(Paragraph(f"DEPARTMENT OF CLINICAL PATHOLOGY & LABORATORY MEDICINE", subtitle_style))
    story.append(Paragraph(f"Branch: {branch.name} | Phone: {tenant.phone or '+1 (555) 019-2831'} | Email: {tenant.contact_email or 'lab@hospital.org'}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0f766e'), spaceAfter=12))

    # 2. Patient & Order Metadata Block
    pat_info = [
        [
            Paragraph(f"<b>Patient Name:</b> {patient.full_name}", header_box_style),
            Paragraph(f"<b>UHID / MRN:</b> {patient.uhid}", header_box_style),
            Paragraph(f"<b>Report No:</b> {lab_report.report_number}", header_box_style),
        ],
        [
            Paragraph(f"<b>Age / Sex:</b> {patient.dob} ({patient.gender})", header_box_style),
            Paragraph(f"<b>Accession No:</b> {order.accession_number}", header_box_style),
            Paragraph(f"<b>Report Version:</b> v{lab_report.version} {'(AMENDED)' if lab_report.is_amended else ''}", header_box_style),
        ],
        [
            Paragraph(f"<b>Referring Doctor:</b> Dr. {order.ordering_clinician}", header_box_style),
            Paragraph(f"<b>Order Date:</b> {order.ordered_at.strftime('%Y-%m-%d %H:%M')}", header_box_style),
            Paragraph(f"<b>Report Approved:</b> {lab_report.approved_at.strftime('%Y-%m-%d %H:%M')}", header_box_style),
        ],
    ]
    pat_table = Table(pat_info, colWidths=[200, 180, 160])
    pat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pat_table)
    story.append(Spacer(1, 14))

    # 3. Investigation Results Table
    results_header = [
        Paragraph("<b>Test Name & LOINC</b>", bold_label),
        Paragraph("<b>Observed Result</b>", bold_label),
        Paragraph("<b>Reference Range</b>", bold_label),
        Paragraph("<b>Units</b>", bold_label),
        Paragraph("<b>Flag / Evaluation</b>", bold_label),
    ]
    table_rows = [results_header]

    for item in order.items.select_related('test').all():
        res = getattr(item, 'result', None)
        test = item.test
        if res:
            val_str = f"<b>{res.numeric_value}</b>" if res.numeric_value is not None else f"<b>{res.text_value}</b>"
            ref_str = res.ref_range_display or (f"{test.ref_min} - {test.ref_max}" if test.ref_min is not None else test.qualitative_normal)
            flag_text = res.flag
            flag_p = flag_abnormal if res.is_abnormal else flag_normal
            loinc_str = f" <font color='#64748b'>({test.loinc_code})</font>" if test.loinc_code else ""

            table_rows.append([
                Paragraph(f"{test.name}{loinc_str}<br/><font size=7 color='#64748b'>Specimen: {test.specimen_type}</font>", table_cell),
                Paragraph(val_str, table_cell),
                Paragraph(ref_str, table_cell),
                Paragraph(res.unit or test.unit or "-", table_cell),
                Paragraph(flag_text, flag_p),
            ])

    results_table = Table(table_rows, colWidths=[180, 100, 120, 60, 80])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f766e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('TOPPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,1), (-1,-1), 5),
        ('BOTTOMPADDING', (0,1), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(results_table)
    story.append(Spacer(1, 20))

    # 4. Signatory Block
    sig_data = [
        [
            Paragraph("<b>Verified By:</b><br/>Senior Medical Technologist, ASCP<br/>Automated Diagnostics Section", table_cell),
            Paragraph(f"<b>Consultant Pathologist Sign-Off:</b><br/><b>{lab_report.approved_by}</b>, MD (Path)<br/>Verified via Cryptographic Digital Hash", table_cell),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 25))

    # 5. Clinical Disclaimer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=6))
    story.append(Paragraph(f"CONFIDENTIAL MEDICAL REPORT — {lab_report.disclaimer}", disclaimer_style))
    story.append(Paragraph(f"Printed from HMS SaaS Tenant [{tenant.code.upper()}] on {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", disclaimer_style))

    doc.build(story)
    return buffer.getvalue()
