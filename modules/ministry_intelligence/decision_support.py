def generate_decision_support(
    health_score,
    comparison,
    recommendations
):

    strengths = []
    opportunities = []
    risks = []
    actions = []
    priorities = []

    if health_score >= 80:
        strengths.append(
            "Ministry health is strong and demonstrates positive leadership indicators."
        )
    else:
        opportunities.append(
            "Ministry health requires focused improvement strategies."
        )

    if comparison:

        if comparison["health_change"] > 0:
            strengths.append(
                "Ministry health is improving compared with the previous assessment."
            )

        if comparison["growth_change"] > 0:
            strengths.append(
                "Growth indicators show positive movement."
            )

        if comparison["current_risk"] == "Low":
            strengths.append(
                "Current ministry risk level is stable."
            )
        else:
            risks.append(
                "Risk level requires leadership attention."
            )

    for item in recommendations:
        opportunities.append(item)

    actions.extend([
        "Review ministry performance indicators regularly.",
        "Strengthen leadership development initiatives.",
        "Use data-driven decisions for ministry planning."
    ])

    priorities.extend([
        "Leadership Development",
        "Member Engagement",
        "Strategic Ministry Growth"
    ])

    return {
        "strengths": strengths,
        "opportunities": opportunities,
        "risks": risks,
        "actions": actions,
        "priorities": priorities
    }
