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
