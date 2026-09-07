from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import (
    MinistryProfile,
    Member,
    ChurchEvent,
    BibleQuiz,
    AIConversation
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

    return render_template(
        "ministry/dashboard.html",
        profile=profile,
        members=members,
        events=events,
        quizzes=quizzes,
        ai_usage=ai_usage
    )
