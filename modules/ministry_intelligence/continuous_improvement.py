def generate_continuous_improvement_plan(
    impact_analysis,
    optimized_recommendations,
    forecast,
    scenarios,
    strategic_plan
):

    performance_review = []
    identified_gaps = []
    improvement_recommendations = []
    learning_feedback = []
    strategy_adjustments = []
    next_action_plan = []

    performance_review.extend([
        "Review ministry outcomes against strategic objectives.",
        "Evaluate effectiveness of implemented actions."
    ])

    identified_gaps.extend([
        "Leadership development opportunities.",
        "Member engagement improvement needs.",
        "Ministry process optimization areas."
    ])

    improvement_recommendations.extend([
        "Strengthen leadership capacity through continuous training.",
        "Improve monitoring of ministry activities.",
        "Use data insights for future decisions."
    ])

    learning_feedback.extend([
        "Capture lessons from ministry implementation.",
        "Apply successful approaches to future initiatives."
    ])

    strategy_adjustments.extend([
        "Refine ministry strategies based on measured outcomes.",
        "Adjust priorities according to emerging needs."
    ])

    next_action_plan.extend([
        "Review current ministry performance.",
        "Implement improvement recommendations.",
        "Measure progress and update strategy."
    ])

    if impact_analysis:
        if impact_analysis.get("improvement_areas"):
            identified_gaps.extend(
                impact_analysis["improvement_areas"]
            )

    if optimized_recommendations:
        if optimized_recommendations.get("action_sequence"):
            next_action_plan.extend(
                optimized_recommendations["action_sequence"]
            )

    return {
        "performance_review": performance_review,
        "identified_gaps": identified_gaps,
        "improvement_recommendations": improvement_recommendations,
        "learning_feedback": learning_feedback,
        "strategy_adjustments": strategy_adjustments,
        "next_action_plan": next_action_plan
    }
