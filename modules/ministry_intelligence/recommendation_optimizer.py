def generate_optimized_recommendations(
    recommendations,
    decision_support,
    strategic_plan,
    forecast,
    scenarios
):

    priority_actions = []
    impact_analysis = []
    urgency_levels = []
    expected_outcomes = []
    action_sequence = []

    for item in recommendations:
        priority_actions.append(
            item
        )

        impact_analysis.append(
            f"Implementing '{item}' can improve ministry effectiveness."
        )

        urgency_levels.append(
            "Medium Priority"
        )

        expected_outcomes.append(
            "Improved ministry performance and leadership capacity."
        )

    action_sequence.extend([
        "1. Assess current ministry condition.",
        "2. Implement priority improvement actions.",
        "3. Monitor progress through ministry intelligence reports.",
        "4. Adjust strategy based on outcomes."
    ])

    if decision_support:
        if decision_support.get("priorities"):
            priority_actions.extend(
                decision_support["priorities"]
            )

    if strategic_plan:
        if strategic_plan.get("immediate_actions"):
            action_sequence.extend(
                strategic_plan["immediate_actions"]
            )

    return {
        "priority_actions": priority_actions,
        "impact_analysis": impact_analysis,
        "urgency_levels": urgency_levels,
        "expected_outcomes": expected_outcomes,
        "action_sequence": action_sequence
    }
