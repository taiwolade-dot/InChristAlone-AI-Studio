from flask import render_template

from . import ministry_intelligence_bp


@ministry_intelligence_bp.route("/ministry-intelligence")
def dashboard():

    ministry_summary = {
        "pastors": 0,
        "churches": 0,
        "events": 0,
        "quiz_participants": 0
    }

    insights = [
        "Ministry Intelligence Dashboard initialized.",
        "Connect Pastor Management, Church Management, Church Calendar and Bible Quiz Analytics."
    ]

    return render_template(
        "ministry_intelligence/dashboard.html",
        summary=ministry_summary,
        insights=insights
    )
