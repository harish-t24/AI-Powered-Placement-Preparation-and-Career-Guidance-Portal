from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_report(student, readiness, filepath):

    doc = SimpleDocTemplate(filepath)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "AI Placement Report",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Name: {student.name}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Email: {student.email}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Aptitude Score: {student.aptitude_score}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Coding Score: {student.coding_score}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Interview Score: {student.interview_score}",
            styles["Normal"]
        )
    )

    elements.append(
        Paragraph(
            f"Resume Score: {student.resume_score}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"Placement Readiness: {readiness}%",
            styles["Heading2"]
        )
    )

    if readiness >= 75:
        recommendation = "Ready for Placement"

    elif readiness >= 50:
        recommendation = "Need More Practice"

    else:
        recommendation = "High Improvement Required"

    elements.append(
        Paragraph(
            f"Recommendation: {recommendation}",
            styles["Heading3"]
        )
    )

    doc.build(elements)