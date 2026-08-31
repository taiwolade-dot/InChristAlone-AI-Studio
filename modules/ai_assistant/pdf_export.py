from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(filename, title, content):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(title, styles["Heading2"])
    )

    story.append(
        Spacer(1, 12)
    )

    story.append(
        Paragraph(
            content.replace("\n","<br/>"),
            styles["BodyText"]
        )
    )

    doc.build(story)
