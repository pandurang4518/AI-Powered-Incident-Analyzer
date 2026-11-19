from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)
from reportlab.lib.utils import simpleSplit


def generate_pdf_report(
    classified_logs,
    incident_logs,
    service_incidents,
    recurring_errors,
    ai_analysis,
    failed_lines
):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=45,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=20,
        textColor=colors.HexColor("#202A44"),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontSize=10,
        textColor=colors.HexColor("#64748B"),
        alignment=TA_CENTER,
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#243B64"),
        spaceBefore=14,
        spaceAfter=8
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    small_style = ParagraphStyle(
        "SmallText",
        parent=styles["BodyText"],
        fontSize=8,
        leading=11
    )

    story = []

    # --------------------------------
    # REPORT HEADER
    # --------------------------------

    story.append(
        Paragraph(
            "PINE LABS | AI INCIDENT ANALYZER",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Application Incident Analysis Report",
            subtitle_style
        )
    )

    report_date = datetime.now().strftime("%d %B %Y, %I:%M %p")

    story.append(
        Paragraph(
            f"<b>Report Generated:</b> {report_date}",
            body_style
        )
    )

    story.append(Spacer(1, 10))

    # --------------------------------
    # INCIDENT OVERVIEW
    # --------------------------------

    story.append(
        Paragraph("1. Incident Overview", heading_style)
    )

    total_logs = len(classified_logs)
    total_incidents = len(incident_logs)
    failed_count = len(failed_lines)

    severity_counts = (
        classified_logs["severity"]
        .value_counts()
        .to_dict()
    )

    overview_data = [
        ["Metric", "Count"],
        ["Total Application Logs", str(total_logs)],
        ["Total Detected Incidents", str(total_incidents)],
        ["Failed Log Entries", str(failed_count)]
    ]

    overview_table = Table(
        overview_data,
        colWidths=[260, 180]
    )

    overview_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F1F5F9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("FONTSIZE", (0, 0), (-1, -1), 9)
    ]))

    story.append(overview_table)

    # --------------------------------
    # SEVERITY SUMMARY
    # --------------------------------

    story.append(
        Paragraph("2. Severity Distribution", heading_style)
    )

    severity_order = ["Critical", "High", "Medium", "Low"]

    severity_data = [["Severity", "Log Count"]]

    for severity in severity_order:
        severity_data.append([
            severity,
            str(severity_counts.get(severity, 0))
        ])

    severity_table = Table(
        severity_data,
        colWidths=[260, 180]
    )

    severity_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("FONTSIZE", (0, 0), (-1, -1), 9)
    ]))

    story.append(severity_table)

    story.append(
        Paragraph(
            "Severity is assigned using predefined rules based on "
            "the application log level.",
            small_style
        )
    )

    # --------------------------------
    # SERVICE ANALYSIS
    # --------------------------------

    story.append(
        Paragraph("3. Incidents by Application Service", heading_style)
    )

    service_data = [["Application Service", "Incident Count"]]

    for _, row in service_incidents.iterrows():
        service_data.append([
            str(row["service"]),
            str(row["incident_count"])
        ])

    if len(service_data) == 1:
        service_data.append(["No incidents", "0"])

    service_table = Table(
        service_data,
        colWidths=[260, 180]
    )

    service_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("FONTSIZE", (0, 0), (-1, -1), 9)
    ]))

    story.append(service_table)

    # --------------------------------
    # RECURRING ERROR PATTERNS
    # --------------------------------

    story.append(
        Paragraph("4. Recurring Error Patterns", heading_style)
    )

    error_data = [["Error Pattern", "Occurrences"]]

    for _, row in recurring_errors.iterrows():
        error_data.append([
            Paragraph(str(row["error_pattern"]), small_style),
            str(row["occurrences"])
        ])

    if len(error_data) == 1:
        error_data.append(["No recurring errors", "0"])

    error_table = Table(
        error_data,
        colWidths=[350, 90],
        repeatRows=1
    )

    error_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#243B64")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("PADDING", (0, 0), (-1, -1), 7),
        ("FONTSIZE", (0, 0), (-1, -1), 8)
    ]))

    story.append(error_table)

    # --------------------------------
    # GEMINI AI ANALYSIS
    # --------------------------------

    story.append(
        Paragraph("5. Gemini AI Incident Analysis", heading_style)
    )

    if ai_analysis:

        for line in ai_analysis.splitlines():

            line = line.strip()

            if not line:
                story.append(Spacer(1, 4))
                continue

            story.append(
                Paragraph(
                    line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"),
                    body_style
                )
            )

    else:

        story.append(
            Paragraph(
                "AI analysis was not generated for this report.",
                body_style
            )
        )

    # --------------------------------
    # DISCLAIMER
    # --------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph("6. Important Note", heading_style)
    )

    story.append(
        Paragraph(
            "This report is generated using a prototype and synthetic "
            "application log data. Severity classifications are "
            "rule-based. Gemini AI findings are potential investigative "
            "hypotheses, not confirmed root causes. All findings require "
            "technical verification.",
            body_style
        )
    )

    # --------------------------------
    # FOOTER
    # --------------------------------

    def add_footer(canvas, doc):

        canvas.saveState()

        canvas.setFont("Helvetica", 8)

        canvas.setFillColor(colors.HexColor("#64748B"))

        canvas.drawString(
            40,
            22,
            "Pine Labs AI Incident Analyzer | Prototype Report"
        )

        canvas.drawRightString(
            A4[0] - 40,
            22,
            f"Page {doc.page}"
        )

        canvas.restoreState()

    document.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    pdf_bytes = buffer.getvalue()

    buffer.close()

    return pdf_bytes