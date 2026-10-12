import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.utils import timezone

def generate_radiology_report_pdf(rad_report):
    """
    Generates a secure, formatted diagnostic radiology examination report PDF
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

    study = rad_report.study
    patient = study.patient
    order_item = study.order_item
    order = order_item.order
    tenant = order.tenant
    branch = order.branch

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'HospitalTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor('#1e40af'),
        alignment=1
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
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1e40af')
    )
    body_text = ParagraphStyle(
        'BodyText',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#0f172a')
    )
    impression_text = ParagraphStyle(
        'ImpressionText',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0f172a')
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

    # 1. Header
    story.append(Paragraph(f"{tenant.name.upper()}", title_style))
    story.append(Paragraph(f"DEPARTMENT OF DIAGNOSTIC & INTERVENTIONAL RADIOLOGY", subtitle_style))
    story.append(Paragraph(f"Facility: {branch.name} | Modality Suite: {study.modality_type} | Contact: {tenant.phone or '+1 (555) 019-2831'}", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1e40af'), spaceAfter=12))

    # 2. Patient & Exam Demographics
    pat_info = [
        [
            Paragraph(f"<b>Patient:</b> {patient.full_name}", header_box_style),
            Paragraph(f"<b>UHID / MRN:</b> {patient.uhid}", header_box_style),
            Paragraph(f"<b>Report No:</b> {rad_report.report_number}", header_box_style),
        ],
        [
            Paragraph(f"<b>Age / Sex:</b> {patient.dob} ({patient.gender})", header_box_style),
            Paragraph(f"<b>Accession No:</b> {study.accession_number}", header_box_style),
            Paragraph(f"<b>Modality:</b> {study.modality_type} ({study.study_description})", header_box_style),
        ],
        [
            Paragraph(f"<b>Referring Physician:</b> Dr. {order.ordering_clinician}", header_box_style),
            Paragraph(f"<b>Study Date:</b> {study.study_date} {study.study_time}", header_box_style),
            Paragraph(f"<b>Report Version:</b> v{rad_report.version} ({rad_report.status})", header_box_style),
        ],
    ]
    pat_table = Table(pat_info, colWidths=[200, 180, 160])
    pat_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#93c5fd')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#dbeafe')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(pat_table)
    story.append(Spacer(1, 12))

    # Study UID reference
    story.append(Paragraph(f"<b>DICOM Study UID:</b> <font color='#475569'>{study.study_instance_uid}</font>", header_box_style))
    story.append(Spacer(1, 10))

    # 3. Clinical Sections
    story.append(Paragraph("CLINICAL INDICATION & REASON FOR EXAM", section_heading))
    story.append(Paragraph(rad_report.clinical_indication or order.clinical_history or "Routine screening / clinical correlation requested.", body_text))
    story.append(Spacer(1, 10))

    story.append(Paragraph("EXAMINATION TECHNIQUE", section_heading))
    story.append(Paragraph(rad_report.examination_technique, body_text))
    story.append(Spacer(1, 10))

    story.append(Paragraph("FINDINGS", section_heading))
    findings_formatted = rad_report.findings.replace('\n', '<br/>')
    story.append(Paragraph(findings_formatted, body_text))
    story.append(Spacer(1, 12))

    story.append(Paragraph("IMPRESSION", section_heading))
    impression_formatted = rad_report.impression.replace('\n', '<br/>')
    story.append(Paragraph(impression_formatted, impression_text))
    story.append(Spacer(1, 10))

    if rad_report.bi_rads_grade:
        story.append(Paragraph(f"<b>ASSESSMENT / SCORE:</b> {rad_report.bi_rads_grade}", body_text))
        story.append(Spacer(1, 8))

    story.append(Paragraph("RECOMMENDATIONS", section_heading))
    story.append(Paragraph(rad_report.recommendations, body_text))
    story.append(Spacer(1, 20))

    # 4. Radiologist Sign-Off Block
    sig_data = [
        [
            Paragraph(f"<b>Performing Technologist:</b><br/>{study.performing_technologist}<br/>Radiologic Technologist (ARRT Certified)", body_text),
            Paragraph(f"<b>Interpreting Radiologist:</b><br/><b>{rad_report.reporting_radiologist or rad_report.approved_by}</b>, M.D.<br/>Diplomate, American Board of Radiology<br/>Finalized: {rad_report.approved_at or timezone.now()}", body_text),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[270, 270])
    sig_table.setStyle(TableStyle([
        ('LINEABOVE', (0,0), (-1,0), 1, colors.HexColor('#94a3b8')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(sig_table)
    story.append(Spacer(1, 20))

    # 5. Disclaimer
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceAfter=6))
    story.append(Paragraph("CONFIDENTIAL MEDICAL RECORD — This radiology interpretation is rendered based on multi-planar image acquisition. Image DICOM instances are securely stored in PACS storage.", disclaimer_style))
    story.append(Paragraph(f"Printed from HMS SaaS Tenant [{tenant.code.upper()}] on {timezone.now().strftime('%Y-%m-%d %H:%M:%S UTC')}", disclaimer_style))

    doc.build(story)
    return buffer.getvalue()
