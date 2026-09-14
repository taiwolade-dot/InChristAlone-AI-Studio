from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_title():

    return "AI Ministry Intelligence Leadership Report"


def add_section(content, title, data, styles):

    content.append(
        Paragraph(
            title,
            styles["Heading2"]
        )
    )

    if isinstance(data, dict):

        for key, value in data.items():

            content.append(
                Paragraph(
                    f"{key.title()}: {value}",
                    styles["Normal"]
                )
            )

    else:

        content.append(
            Paragraph(
                str(data),
                styles["Normal"]
            )
        )

    content.append(
        Spacer(1, 12)
    )


def build_pdf_content(document):

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            generate_pdf_title(),
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    metadata = document.get(
        "metadata",
        {}
    )

    add_section(
        content,
        "Report Metadata",
        metadata,
        styles
    )

    sections = document.get(
        "sections",
        {}
    )

    add_section(
        content,
        "Ministry Overview",
        sections.get("overview", {}),
        styles
    )

    intelligence = sections.get(
        "intelligence",
        {}
    )

    add_section(
        content,
        "Health Intelligence",
        {
            "health_score": intelligence.get(
                "health_score",
                0
            )
        },
        styles
    )

    add_section(
        content,
        "Network Intelligence",
        intelligence.get(
            "network",
            {}
        ),
        styles
    )

    add_section(
        content,
        "Growth Forecast",
        intelligence.get(
            "forecast",
            {}
        ),
        styles
    )

    actions = sections.get(
        "actions",
        {}
    )

    add_section(
        content,
        "Risk Assessment",
        actions.get(
            "alerts",
            {}
        ),
        styles
    )

    add_section(
        content,
        "Strategic Action Plan",
        actions.get(
            "strategies",
            {}
        ),
        styles
    )

    return content


def generate_pdf_report(document, filename):

    pdf = SimpleDocTemplate(
        filename
    )

    content = build_pdf_content(
        document
    )

    pdf.build(
        content
    )

    return filename
