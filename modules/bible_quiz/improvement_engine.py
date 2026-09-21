def generate_quiz_improvement(analytics):

    recommendations = []

    for item in analytics:

        if item.accuracy_rate < 50:
            recommendations.append({
                "question_id": item.question_id,
                "action": "simplify",
                "reason": "Low learner understanding detected"
            })

        elif item.accuracy_rate > 90:
            recommendations.append({
                "question_id": item.question_id,
                "action": "increase_difficulty",
                "reason": "Learners mastered this concept"
            })

        else:
            recommendations.append({
                "question_id": item.question_id,
                "action": "maintain",
                "reason": "Balanced learning challenge"
            })

    return recommendations
