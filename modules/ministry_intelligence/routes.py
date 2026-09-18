import json
import os
from datetime import datetime

from flask import render_template, send_file

from . import ministry_intelligence_bp
from .services import get_ministry_summary
from .intelligence import generate_ministry_insights
from .health import calculate_ministry_health
from .analytics import generate_ministry_analytics
from .recommendations import generate_ministry_recommendations
from .health_insights import generate_health_insights
from .comparative import generate_comparative_report
from .association import generate_network_report
from .prediction import generate_prediction_report
from .alerts import generate_alert_report
from .strategy import generate_strategy_report
from .report import generate_ministry_report
from .export import generate_export_report
from .documents import generate_ministry_document
from .pdf_generator import generate_pdf_report
from .report_manager import create_report_record, get_report_history, get_report_by_id, get_report_statistics
from .comparison_manager import compare_reports
from .decision_support import generate_decision_support
from .strategic_planner import generate_strategic_plan
from .forecasting import generate_ministry_forecast
from .scenario_simulator import generate_ministry_scenarios
from .recommendation_optimizer import generate_optimized_recommendations
from .impact_analyzer import generate_ministry_impact_analysis
from .continuous_improvement import generate_continuous_improvement_plan
from .knowledge_engine import generate_ministry_knowledge_insights
from .prediction import generate_predictive_ministry_insights

from modules.ai_assistant.member_intelligence import (
    get_ministry_care_statistics,
    get_top_engaged_members,
    get_members_needing_attention
)



@ministry_intelligence_bp.route("/ministry-intelligence")
def dashboard():

    ministry_summary = get_ministry_summary()

    care_statistics = get_ministry_care_statistics()

    top_engaged_members = get_top_engaged_members()

    members_needing_attention = get_members_needing_attention()

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

    comparative_report = generate_comparative_report()

    network_report = generate_network_report()

    prediction_report = generate_prediction_report(
        ministry_summary,
        analytics,
        health_score
    )

    alert_report = generate_alert_report(
        ministry_summary
    )

    strategy_report = generate_strategy_report(
        prediction_report,
        alert_report
    )

    ministry_report = generate_ministry_report(
        ministry_summary,
        health_score,
        network_report,
        prediction_report,
        alert_report,
        strategy_report
    )

    export_report = generate_export_report(
        ministry_report
    )

    return render_template(
        "ministry_intelligence/dashboard.html",
        summary=ministry_summary,
        insights=insights,
        health_score=health_score,
        health_insights=health_insights,
        analytics=analytics,
        chart_data=json.dumps(chart_data),
        recommendations=recommendations,
        comparative_report=comparative_report,
        network_report=network_report,
        prediction_report=prediction_report,
        alert_report=alert_report,
        strategy_report=strategy_report,
        ministry_report=ministry_report,
        export_report=export_report,
        care_statistics=care_statistics,
        top_engaged_members=top_engaged_members,
        members_needing_attention=members_needing_attention
    )


@ministry_intelligence_bp.route("/download-ministry-report")
def download_ministry_report():

    ministry_summary = get_ministry_summary()

    health_score = calculate_ministry_health(
        ministry_summary
    )

    analytics = generate_ministry_analytics()

    network_report = generate_network_report()

    prediction_report = generate_prediction_report(
        ministry_summary,
        analytics,
        health_score
    )

    alert_report = generate_alert_report(
        ministry_summary
    )

    strategy_report = generate_strategy_report(
        prediction_report,
        alert_report
    )

    ministry_report = generate_ministry_report(
        ministry_summary,
        health_score,
        network_report,
        prediction_report,
        alert_report,
        strategy_report
    )

    export_report = generate_export_report(
        ministry_report
    )

    document = generate_ministry_document(
        export_report
    )

    filename = (
        "reports/ministry_intelligence/"
        f"AI_Ministry_Intelligence_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    generate_pdf_report(
        document,
        filename
    )

    create_report_record(
        title=document.get("title"),
        report_type="Ministry Intelligence",
        generated_by=document.get("metadata", {}).get("generated_by"),
        generated_on=document.get("metadata", {}).get("generated_on"),
        file_path=filename
    )

    return send_file(
        filename,
        as_attachment=True,
        download_name=filename
    )




@ministry_intelligence_bp.route("/ministry-report-comparison")
def ministry_report_comparison():

    reports = get_report_history()

    comparison = None

    if len(reports) >= 2:
        comparison = compare_reports(
            reports[1].id,
            reports[0].id
        )

    return render_template(
        "ministry_intelligence/comparison.html",
        reports=reports,
        comparison=comparison
    )



@ministry_intelligence_bp.route("/ministry-executive-dashboard")
def ministry_executive_dashboard():

    ministry_summary = get_ministry_summary()

    health_score = calculate_ministry_health(
        ministry_summary
    )

    statistics = get_report_statistics()

    reports = get_report_history()

    comparison = None

    if len(reports) >= 2:
        comparison = compare_reports(
            reports[1].id,
            reports[0].id
        )

    recommendations = generate_ministry_recommendations(
        ministry_summary,
        generate_ministry_analytics()
    )

    decision_support = generate_decision_support(
        health_score,
        comparison,
        recommendations
    )

    strategic_plan = generate_strategic_plan(
        health_score,
        decision_support
    )

    forecast = generate_ministry_forecast(
        health_score,
        comparison,
        generate_ministry_analytics(),
        strategic_plan
    )

    scenarios = generate_ministry_scenarios(
        forecast,
        strategic_plan,
        decision_support
    )

    optimized_recommendations = generate_optimized_recommendations(
        recommendations,
        decision_support,
        strategic_plan,
        forecast,
        scenarios
    )

    impact_analysis = generate_ministry_impact_analysis(
        health_score,
        comparison,
        forecast,
        scenarios,
        optimized_recommendations
    )

    continuous_improvement = generate_continuous_improvement_plan(
        impact_analysis,
        optimized_recommendations,
        forecast,
        scenarios,
        strategic_plan
    )

    knowledge_insights = generate_ministry_knowledge_insights(
        comparison,
        forecast,
        impact_analysis,
        continuous_improvement
    )

    predictive_insights = generate_predictive_ministry_insights(
        forecast,
        scenarios,
        knowledge_insights,
        impact_analysis,
        continuous_improvement
    )

    chart_data = {
        "health_change": comparison["health_change"] if comparison else 0,
        "growth_change": comparison["growth_change"] if comparison else 0,
        "previous_health": (
            health_score - comparison["health_change"]
            if comparison else health_score
        ),
        "current_health": health_score
    }

    return render_template(
        "ministry_intelligence/executive_dashboard.html",
        health_score=health_score,
        statistics=statistics,
        comparison=comparison,
        recommendations=recommendations,
        decision_support=decision_support,
        strategic_plan=strategic_plan,
        forecast=forecast,
        scenarios=scenarios,
        optimized_recommendations=optimized_recommendations,
        impact_analysis=impact_analysis,
        continuous_improvement=continuous_improvement,
        knowledge_insights=knowledge_insights,
        predictive_insights=predictive_insights,
        chart_data=json.dumps(chart_data)
    )

@ministry_intelligence_bp.route("/ministry-reports")
def ministry_reports():

    reports = get_report_history()
    statistics = get_report_statistics()

    return render_template(
        "ministry_intelligence/reports.html",
        reports=reports,
        statistics=statistics
    )


@ministry_intelligence_bp.route("/download-report/<int:report_id>")
def download_report(report_id):

    report = get_report_by_id(report_id)

    if not report:
        return "Report not found", 404

    return send_file(
        report.file_path,
        as_attachment=True,
        download_name=report.file_path.split("/")[-1]
    )
