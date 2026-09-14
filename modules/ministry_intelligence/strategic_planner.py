def generate_strategic_plan(
    health_score,
    decision_support
):

    immediate_actions = []
    growth_strategy = []
    leadership_plan = []
    outreach_plan = []
    discipleship_plan = []

    if health_score >= 80:
        immediate_actions.append(
            "Maintain current ministry momentum through consistent evaluation."
        )
    else:
        immediate_actions.append(
            "Prioritize ministry health improvement initiatives."
        )

    growth_strategy.extend([
        "Develop measurable ministry growth objectives.",
        "Strengthen member engagement systems.",
        "Review ministry performance quarterly."
    ])

    leadership_plan.extend([
        "Invest in leadership training and mentoring.",
        "Identify emerging ministry leaders."
    ])

    outreach_plan.extend([
        "Improve community engagement activities.",
        "Develop structured outreach follow-up."
    ])

    discipleship_plan.extend([
        "Strengthen Bible teaching programs.",
        "Encourage continuous spiritual growth."
    ])

    if decision_support.get("priorities"):
        growth_strategy.extend(
            decision_support["priorities"]
        )

    return {
        "immediate_actions": immediate_actions,
        "growth_strategy": growth_strategy,
        "leadership_plan": leadership_plan,
        "outreach_plan": outreach_plan,
        "discipleship_plan": discipleship_plan
    }
