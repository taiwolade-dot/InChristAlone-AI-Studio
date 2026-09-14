def generate_document_title():

    return "AI Ministry Intelligence Leadership Report"


def generate_document_sections(export_report):

    return {
        "overview": export_report.get(
            "report",
            {}
        ).get(
            "overview",
            {}
        ),

        "intelligence": export_report.get(
            "intelligence",
            {}
        ),

        "actions": export_report.get(
            "actions",
            {}
        )
    }


def generate_ministry_document(export_report):

    return {
        "title": generate_document_title(),
        "metadata": export_report.get(
            "report",
            {}
        ).get(
            "metadata",
            {}
        ),
        "sections": generate_document_sections(
            export_report
        )
    }
