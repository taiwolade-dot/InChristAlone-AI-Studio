from models import MinistryReportAnalysis


def compare_reports(previous_report_id, current_report_id):

    previous = MinistryReportAnalysis.query.filter_by(
        report_id=previous_report_id
    ).first()

    current = MinistryReportAnalysis.query.filter_by(
        report_id=current_report_id
    ).first()

    if not previous or not current:
        return None

    return {
        "health_change": current.health_score - previous.health_score,
        "growth_change": current.growth_score - previous.growth_score,
        "previous_risk": previous.risk_level,
        "current_risk": current.risk_level,
        "recommendation_change": current.recommendations
    }
