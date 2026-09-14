from flask import render_template

from . import ministry_intelligence_bp
from .services import get_ministry_summary
from .intelligence import generate_ministry_insights
from .health import calculate_ministry_health
from .analytics import generate_ministry_analytics


@ministry_intelligence_bp.route("/ministry-intelligence")
def dashboard():

    ministry_summary = get_ministry_summary()

    insights = generate_ministry_insights(
        ministry_summary
    )

    health_score = calculate_ministry_health(
        ministry_summary
    )

    analytics = generate_ministry_analytics()

    return render_template(
        "ministry_intelligence/dashboard.html",
        summary=ministry_summary,
        insights=insights,
        health_score=health_score,
        analytics=analytics
    )
