def generate_ministry_forecast(
    health_score,
    comparison,
    analytics,
    strategic_plan
):

    growth_forecast = []
    membership_outlook = []
    leadership_forecast = []
    risk_projection = []
    scenarios = []

    if health_score >= 80:
        growth_forecast.append(
            "Ministry indicators suggest continued positive development."
        )
    else:
        growth_forecast.append(
            "Ministry growth requires focused improvement initiatives."
        )

    membership_outlook.append(
        "Membership growth depends on engagement, follow-up, and discipleship systems."
    )

    leadership_forecast.append(
        "Leadership capacity can improve through structured development programs."
    )

    if comparison:
        if comparison["health_change"] < 0:
            risk_projection.append(
                "Declining health indicators require immediate attention."
            )
        else:
            risk_projection.append(
                "Current trend indicators show manageable ministry risk."
            )

    scenarios.extend([
        "Optimistic Scenario: Strong engagement leads to sustained growth.",
        "Development Scenario: Strategic improvements produce gradual progress.",
        "Challenge Scenario: Limited engagement slows ministry advancement."
    ])

    if strategic_plan:
        growth_forecast.extend(
            strategic_plan.get("growth_strategy", [])
        )

    return {
        "growth_forecast": growth_forecast,
        "membership_outlook": membership_outlook,
        "leadership_forecast": leadership_forecast,
        "risk_projection": risk_projection,
        "scenarios": scenarios
    }
