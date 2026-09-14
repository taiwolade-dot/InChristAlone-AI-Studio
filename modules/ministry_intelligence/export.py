from datetime import datetime


def generate_report_title():

    return "AI Ministry Intelligence Report"


def generate_report_metadata():

    return {
        "generated_on": datetime.now().strftime("%Y-%m-%d"),
        "generated_by": "InChristAlone AI Studio",
        "report_type": "Ministry Intelligence"
    }


def generate_export_summary(ministry_report):

    executive = ministry_report.get(
        "executive_summary",
        {}
    )

    return {
        "title": generate_report_title(),
        "metadata": generate_report_metadata(),
        "overview": {
            "churches": executive.get("churches", 0),
            "members": executive.get("members", 0),
            "pastors": executive.get("pastors", 0),
            "events": executive.get("events", 0)
        }
    }


def generate_export_report(ministry_report):

    return {
        "report": generate_export_summary(
            ministry_report
        ),
        "intelligence": ministry_report.get(
            "intelligence_summary",
            {}
        ),
        "actions": ministry_report.get(
            "action_summary",
            {}
        )
    }
