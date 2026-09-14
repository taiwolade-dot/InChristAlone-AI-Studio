def generate_ministry_scenarios(
    forecast,
    strategic_plan,
    decision_support
):

    growth_scenario = []
    stability_scenario = []
    risk_scenario = []
    intervention_scenario = []
    recommended_path = []

    growth_scenario.extend([
        "Increased engagement may lead to stronger ministry growth.",
        "Consistent discipleship and outreach can improve future outcomes."
    ])

    stability_scenario.extend([
        "Current ministry patterns may continue with gradual progress.",
        "Regular monitoring will help maintain stability."
    ])

    risk_scenario.extend([
        "Reduced engagement may affect ministry effectiveness.",
        "Leadership gaps may slow ministry advancement."
    ])

    intervention_scenario.extend([
        "Applying strategic recommendations can improve ministry direction.",
        "Leadership development can strengthen future capacity."
    ])

    recommended_path.extend([
        "Prioritize leadership development.",
        "Strengthen member engagement systems.",
        "Implement measurable ministry improvement goals."
    ])

    if forecast:
        if forecast.get("growth_forecast"):
            growth_scenario.extend(
                forecast["growth_forecast"]
            )

    if strategic_plan:
        if strategic_plan.get("growth_strategy"):
            intervention_scenario.extend(
                strategic_plan["growth_strategy"]
            )

    if decision_support:
        if decision_support.get("priorities"):
            recommended_path.extend(
                decision_support["priorities"]
            )

    return {
        "growth_scenario": growth_scenario,
        "stability_scenario": stability_scenario,
        "risk_scenario": risk_scenario,
        "intervention_scenario": intervention_scenario,
        "recommended_path": recommended_path
    }
