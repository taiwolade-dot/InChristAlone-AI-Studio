def generate_growth_forecast(summary, analytics):

    forecast = {
        "direction": "Stable",
        "confidence": "Low",
        "message": ""
    }

    members = summary.get("members", 0)
    events = summary.get("events", 0)

    if members > 0 and events > 0:
        forecast["direction"] = "Positive"
        forecast["confidence"] = "Moderate"
        forecast["message"] = (
            "Current ministry records indicate potential for continued growth."
        )

    elif members > 0:
        forecast["direction"] = "Slow Growth"
        forecast["confidence"] = "Low"
        forecast["message"] = (
            "Membership records exist, but ministry activity needs strengthening."
        )

    else:
        forecast["direction"] = "Needs Data"
        forecast["confidence"] = "Very Low"
        forecast["message"] = (
            "Additional ministry records are needed for accurate forecasting."
        )

    return forecast


def generate_health_forecast(health_score):

    if health_score >= 80:
        return {
            "status": "Strong",
            "message": "Ministry health indicators show strong readiness."
        }

    elif health_score >= 50:
        return {
            "status": "Developing",
            "message": "Ministry systems are developing and require attention."
        }

    return {
        "status": "Needs Attention",
        "message": "Priority improvement areas should be addressed."
    }


def generate_prediction_report(summary, analytics, health_score):

    return {
        "growth_forecast": generate_growth_forecast(
            summary,
            analytics
        ),
        "health_forecast": generate_health_forecast(
            health_score
        )
    }


def generate_predictive_ministry_insights(
    forecast,
    scenarios,
    knowledge_insights,
    impact_analysis,
    continuous_improvement
):

    growth_predictions = []
    risk_predictions = []
    trend_analysis = []
    future_outcomes = []
    early_warning_signals = []
    predictive_recommendations = []

    growth_predictions.extend([
        "Ministry growth potential depends on consistent leadership and member engagement.",
        "Strategic implementation may improve future ministry outcomes."
    ])

    risk_predictions.extend([
        "Leadership capacity gaps may slow ministry progress.",
        "Insufficient monitoring may reduce strategy effectiveness."
    ])

    trend_analysis.extend([
        "Data-driven ministry decisions are becoming increasingly important.",
        "Continuous evaluation supports sustainable ministry development."
    ])

    future_outcomes.extend([
        "Improved planning can produce stronger ministry effectiveness.",
        "Knowledge-based decisions can increase long-term ministry resilience."
    ])

    early_warning_signals.extend([
        "Declining participation patterns require attention.",
        "Unresolved leadership challenges may affect future outcomes."
    ])

    predictive_recommendations.extend([
        "Monitor ministry indicators regularly.",
        "Use previous learning patterns to guide future decisions.",
        "Adjust strategies before challenges become critical."
    ])

    if knowledge_insights:
        if knowledge_insights.get("adaptive_recommendations"):
            predictive_recommendations.extend(
                knowledge_insights["adaptive_recommendations"]
            )

    if impact_analysis:
        if impact_analysis.get("improvement_areas"):
            risk_predictions.extend(
                impact_analysis["improvement_areas"]
            )

    if continuous_improvement:
        if continuous_improvement.get("next_action_plan"):
            future_outcomes.extend(
                continuous_improvement["next_action_plan"]
            )

    return {
        "growth_predictions": growth_predictions,
        "risk_predictions": risk_predictions,
        "trend_analysis": trend_analysis,
        "future_outcomes": future_outcomes,
        "early_warning_signals": early_warning_signals,
        "predictive_recommendations": predictive_recommendations
    }
