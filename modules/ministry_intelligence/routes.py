import json

from flask import render_template

from . import ministry_intelligence_bp
from .services import get_ministry_summary
from .intelligence import generate_ministry_insights
from .health import calculate_ministry_health
from .analytics import generate_ministry_analytics
from .recommendations import generate_ministry_recommendations
from .health_insights import generate_health_insights


@ministry_intelligence_bp.route("/ministry-intelligence")
def dashboard():

    ministry_summary = get_ministry_summary()

    insights = generate_ministry_insights(
        ministry_summary
    )

    health_score = calculate_ministry_health(
        ministry_summary
    )

    health_insights = generate_health_insights(
        ministry_summary
    )

    analytics = generate_ministry_analytics()

    chart_data = {
        "member_growth": analytics["member_growth"],
        "event_activity": analytics["event_activity"]
    }

    recommendations = generate_ministry_recommendations(
        ministry_summary,
        analytics
    )

    return render_template(
        "ministry_intelligence/dashboard.html",
        summary=ministry_summary,
        insights=insights,
        health_score=health_score,
        health_insights=health_insights,
        analytics=analytics,
        chart_data=json.dumps(chart_data),
        recommendations=recommendations
    )
