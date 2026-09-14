from datetime import datetime

from models import db, MinistryReport


def create_report_record(
    title,
    report_type,
    generated_by,
    generated_on,
    file_path
):

    report = MinistryReport(
        title=title,
        report_type=report_type,
        generated_by=generated_by,
        generated_on=generated_on,
        file_path=file_path
    )

    db.session.add(report)
    db.session.commit()

    return report


def get_report_history():

    return MinistryReport.query.order_by(
        MinistryReport.created_at.desc()
    ).all()


def get_report_by_id(report_id):

    return MinistryReport.query.get(
        report_id
    )


def get_report_statistics():

    reports = MinistryReport.query.all()

    total_reports = len(reports)

    latest_report = None

    if reports:
        latest_report = max(
            reports,
            key=lambda report: report.created_at
        )

    report_types = len(
        set(
            report.report_type
            for report in reports
        )
    )

    return {
        "total_reports": total_reports,
        "latest_report": latest_report,
        "report_types": report_types
    }
