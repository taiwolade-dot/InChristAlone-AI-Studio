from models import (
    PastorProfile,
    ChurchProfile,
    Member,
    ChurchEvent,
    QuizParticipant,
    QuizQuestionAnalytics,
    ActivityLog,
    MinistryContent
)


def get_ministry_summary():

    summary = {
        "pastors": PastorProfile.query.count(),
        "churches": ChurchProfile.query.count(),
        "members": Member.query.count(),
        "events": ChurchEvent.query.count(),
        "quiz_participants": QuizParticipant.query.count()
    }

    summary["member_ai_activities"] = ActivityLog.query.count()

    summary["birthday_interactions"] = ActivityLog.query.filter(
        ActivityLog.action.like("Birthday%")
    ).count()

    summary["ai_content_generated"] = MinistryContent.query.count()

    analytics = QuizQuestionAnalytics.query.all()

    if analytics:
        summary["quiz_accuracy"] = round(
            sum(a.accuracy_rate for a in analytics) / len(analytics),
            2
        )
    else:
        summary["quiz_accuracy"] = 0

    return summary
