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
