from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
import os

def generate_pdf(metrics, folder):
    filename = f"{folder}Plato_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    doc = SimpleDocTemplate(filename)
    elements = []

    style = ParagraphStyle(
        name='Normal',
        fontName='Helvetica',
        fontSize=10,
        textColor=colors.black
    )

    elements.append(Paragraph("Plato Capital System Report", style))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Paragraph(f"Average Return: {metrics['avg_return']:.2f}", style))
    elements.append(Paragraph(f"Success Rate: {metrics['success_rate']:.2f}%", style))
    elements.append(Paragraph(f"Confidence Correlation: {metrics['confidence_corr']:.2f}", style))
    elements.append(Paragraph(f"Time Correlation: {metrics['time_corr']:.2f}", style))

    doc.build(elements)

    return filename
