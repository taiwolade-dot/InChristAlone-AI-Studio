from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, date

from models import (
    MinistryProfile,
    Member,
    ChurchEvent,
    BibleQuiz,
    AIConversation,
    MinistryOccasion
)


ministry_bp = Blueprint(
    "ministry",
    __name__,
    url_prefix="/ministry"
)


@ministry_bp.route("/")
@login_required
def dashboard():

    profile = MinistryProfile.query.filter_by(
        user_id=current_user.id
    ).first()

    members = Member.query.filter_by(
        owner_id=current_user.id
    ).count()

    events = ChurchEvent.query.filter_by(
        created_by=current_user.id
    ).count()

    quizzes = BibleQuiz.query.filter_by(
        owner_id=current_user.id
    ).count()

    ai_usage = AIConversation.query.filter_by(
        user_id=current_user.id
    ).count()

    today = date.today()

    upcoming_events = ChurchEvent.query.filter(
        ChurchEvent.created_by == current_user.id,
        ChurchEvent.start_datetime >= datetime.utcnow()
    ).order_by(
        ChurchEvent.start_datetime.asc()
    ).limit(5).all()

    event_alerts = []

    for event in upcoming_events:
        days_remaining = (event.start_datetime.date() - today).days
        event.days_remaining = days_remaining

        if days_remaining in [30, 7, 1]:
            event_alerts.append({
                "id": event.id,
                "title": event.title,
                "days_remaining": days_remaining
            })

    birthday_alerts = []

    members_with_birthdays = Member.query.filter_by(
        owner_id=current_user.id
    ).all()

    for member in members_with_birthdays:
        if member.birthday:
            birthday_this_year = member.birthday.replace(
                year=today.year
            )

            days_until = (birthday_this_year - today).days

            if days_until < 0:
                days_until += 365

            if days_until <= 7:
                birthday_alerts.append({
                    "name": member.full_name,
                      "member_id": member.id,
                    "days_remaining": days_until
            })

    occasion_alerts = []

    upcoming_occasions = MinistryOccasion.query.filter(
        MinistryOccasion.created_by == current_user.id,
        MinistryOccasion.date >= today
    ).order_by(
        MinistryOccasion.date.asc()
    ).limit(5).all()

    for occasion in upcoming_occasions:
        days_remaining = (
            occasion.date - today
        ).days

        occasion_alerts.append({
            "id": occasion.id,
            "title": occasion.title,
            "occasion_type": occasion.occasion_type,
            "days_remaining": days_remaining
        })

    return render_template(
        "ministry/dashboard.html",
        profile=profile,
        members=members,
        events=events,
        quizzes=quizzes,
        ai_usage=ai_usage,
          upcoming_events=upcoming_events,
          event_alerts=event_alerts,
          birthday_alerts=birthday_alerts,
        occasion_alerts=occasion_alerts
    )
