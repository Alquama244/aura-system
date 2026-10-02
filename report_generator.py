import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_excel(object_counts, ai_analysis):
    """
    Generates an Excel report in-memory and returns bytes for download.
    """
    output = io.BytesIO()
    
    items = list(object_counts.items()) if object_counts else [("No objects detected", 0)]
    df_counts = pd.DataFrame(items, columns=["Item / Category", "Count"])
    df_summary = pd.DataFrame([{"AI Narrative Analysis": ai_analysis}])

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_counts.to_excel(writer, sheet_name='Inventory Counts', index=False)
        df_summary.to_excel(writer, sheet_name='AI Narrative', index=False)

    output.seek(0)
    return output.getvalue()

def generate_pdf(object_counts, ai_analysis):
    """
    Generates a PDF report in-memory and returns bytes for download.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E3A8A'),
        spaceAfter=12
    )
    story.append(Paragraph("AURA Visual Inventory & Intelligence Report", title_style))
    story.append(Spacer(1, 12))

    story.append(Paragraph("<b>1. Object Detection Counts</b>", styles['Heading2']))
    story.append(Spacer(1, 6))

    table_data = [["Item / Category", "Quantity"]]
    if object_counts:
        for item, count in object_counts.items():
            table_data.append([str(item).title(), str(count)])
    else:
        table_data.append(["No objects detected", "0"])

    t = Table(table_data, colWidths=[250, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#F3F4F6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
    ]))
    story.append(t)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>2. Generative AI Narrative Analysis</b>", styles['Heading2']))
    story.append(Spacer(1, 6))

    formatted_analysis = ai_analysis.replace('\n', '<br/>')
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1F2937')
    )
    story.append(Paragraph(formatted_analysis, body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
