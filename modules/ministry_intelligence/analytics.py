from collections import Counter

from models import (
    Member,
    ChurchEvent,
    QuizParticipant
)


def member_growth_analysis():

    members = Member.query.all()

    monthly_growth = Counter()

    for member in members:
        if member.created_at:
            month = member.created_at.strftime("%Y-%m")
            monthly_growth[month] += 1

    return dict(monthly_growth)


def event_activity_analysis():

    events = ChurchEvent.query.all()

    monthly_events = Counter()

    for event in events:
        if event.start_datetime:
            month = event.start_datetime.strftime("%Y-%m")
            monthly_events[month] += 1

    return dict(monthly_events)


def quiz_engagement_analysis():

    participants = QuizParticipant.query.count()

    return {
        "total_participants": participants
    }


def generate_ministry_analytics():

    return {
        "member_growth": member_growth_analysis(),
        "event_activity": event_activity_analysis(),
        "quiz_engagement": quiz_engagement_analysis()
    }
