from modules.ministry_intelligence.services import get_ministry_summary
from modules.ministry_intelligence.health import calculate_ministry_health
from modules.ministry_intelligence.analytics import generate_ministry_analytics
from modules.ministry_intelligence.comparative import generate_comparative_report
from modules.ministry_intelligence.recommendations import generate_ministry_recommendations
from modules.ministry_intelligence.decision_support import generate_decision_support
from modules.ministry_intelligence.strategic_planner import generate_strategic_plan
from modules.ministry_intelligence.forecasting import generate_ministry_forecast
from modules.ministry_intelligence.scenario_simulator import generate_ministry_scenarios
from modules.ministry_intelligence.recommendation_optimizer import generate_optimized_recommendations
from modules.ministry_intelligence.impact_analyzer import generate_ministry_impact_analysis
from modules.ministry_intelligence.continuous_improvement import generate_continuous_improvement_plan
from modules.ministry_intelligence.knowledge_engine import generate_ministry_knowledge_insights
from modules.ministry_intelligence.prediction import generate_predictive_ministry_insights
from .memory_engine import summarize_ministry_memory




def build_forecast_comparison(comparison_report):

    return {
        "health_change": 0,
        "growth_change": 0,
        "current_risk": "Low"
    }


def generate_ministry_copilot_context():

    summary = get_ministry_summary()

    health = calculate_ministry_health(summary)

    analytics = generate_ministry_analytics()

    memory_context = summarize_ministry_memory()

    comparison_report = generate_comparative_report()

    comparison = build_forecast_comparison(comparison_report)

    recommendations = generate_ministry_recommendations(
        summary,
        analytics
    )

    decision_support = generate_decision_support(
        health,
        None,
        recommendations
    )

    strategic_plan = generate_strategic_plan(
        health,
        decision_support
    )

    forecast = generate_ministry_forecast(
        health,
        comparison,
        analytics,
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
        health,
        comparison,
        forecast,
        scenarios,
        optimized_recommendations
    )

    improvement = generate_continuous_improvement_plan(
        impact_analysis,
        optimized_recommendations,
        forecast,
        scenarios,
        strategic_plan
    )

    knowledge = generate_ministry_knowledge_insights(
        comparison,
        forecast,
        impact_analysis,
        improvement
    )

    predictions = generate_predictive_ministry_insights(
        summary,
        analytics,
        knowledge,
        impact_analysis,
        improvement
    )

    return {
        "summary": summary,
        "health": health,
        "analytics": analytics,
        "recommendations": recommendations,
        "decision_support": decision_support,
        "strategic_plan": strategic_plan,
        "forecast": forecast,
        "scenarios": scenarios,
        "optimized_recommendations": optimized_recommendations,
        "impact_analysis": impact_analysis,
        "continuous_improvement": improvement,
        "knowledge": knowledge,
        "predictions": predictions,
        "memory_context": memory_context
    }


def format_ministry_copilot_response():

    context = generate_ministry_copilot_context()

    return f"""
🧠 AI Ministry Copilot

Ministry Summary:
{context['summary']}

Ministry Health:
{context['health']}

Strategic Recommendations:
{context['recommendations']}

Knowledge Insights:
{context['knowledge']}

Predictive Insights:
{context['predictions']}
"""
