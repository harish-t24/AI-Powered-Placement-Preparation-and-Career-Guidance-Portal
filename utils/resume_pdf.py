from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

def create_resume_pdf(
    content,
    filepath
):

    doc = SimpleDocTemplate(
        filepath
    )

    styles = getSampleStyleSheet()

    elements = []

    for line in content.split("\n"):

        if line.strip():

            elements.append(
                Paragraph(
                    line,
                    styles["Normal"]
                )
            )

            elements.append(
                Spacer(1,6)
            )

    doc.build(elements)