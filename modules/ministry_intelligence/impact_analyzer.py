def generate_ministry_impact_analysis(
    health_score,
    comparison,
    forecast,
    scenarios,
    optimized_recommendations
):

    impact_score = []
    improvement_areas = []
    success_indicators = []
    effectiveness_analysis = []
    continuous_improvement = []

    if health_score >= 80:
        impact_score.append(
            "High potential for positive ministry impact."
        )
    elif health_score >= 50:
        impact_score.append(
            "Moderate ministry impact potential with focused improvement."
        )
    else:
        impact_score.append(
            "Low impact indicators require strategic intervention."
        )

    improvement_areas.extend([
        "Leadership capacity development.",
        "Member engagement improvement.",
        "Ministry system strengthening."
    ])

    success_indicators.extend([
        "Improved ministry participation.",
        "Stronger leadership effectiveness.",
        "Consistent achievement of ministry objectives."
    ])

    effectiveness_analysis.extend([
        "Evaluate implemented strategies against expected outcomes.",
        "Compare ministry progress with previous assessments."
    ])

    continuous_improvement.extend([
        "Review ministry performance regularly.",
        "Refine strategies based on measured outcomes.",
        "Maintain a culture of continuous improvement."
    ])

    if optimized_recommendations:
        if optimized_recommendations.get("priority_actions"):
            effectiveness_analysis.append(
                "Priority actions provide measurable improvement pathways."
            )

    return {
        "impact_score": impact_score,
        "improvement_areas": improvement_areas,
        "success_indicators": success_indicators,
        "effectiveness_analysis": effectiveness_analysis,
        "continuous_improvement": continuous_improvement
    }
