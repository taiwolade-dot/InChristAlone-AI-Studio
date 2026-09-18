from models import ActivityLog, MinistryContent


def get_member_ai_history(member_name, limit=10):
    activities = ActivityLog.query.filter(
        ActivityLog.details.contains(member_name)
    ).order_by(
        ActivityLog.created_at.desc()
    ).limit(limit).all()

    content = MinistryContent.query.filter(
        MinistryContent.title.contains(member_name)
    ).order_by(
        MinistryContent.created_at.desc()
    ).limit(limit).all()

    history = []

    for item in activities:
        history.append({
            "type": "AI Activity",
            "title": item.action,
            "date": item.created_at
        })

    for item in content:
        history.append({
            "type": "AI Content",
            "title": item.title,
            "date": item.created_at
        })

    history.sort(
        key=lambda x: x["date"],
        reverse=True
    )

    return history[:limit]


def get_member_ai_summary(member_name):
    history = get_member_ai_history(member_name)

    return {
        "total_interactions": len(history),
        "last_interaction": history[0]["date"] if history else None,
        "history": history
    }


def calculate_member_care_score(member_name):
    history = get_member_ai_history(member_name, limit=50)

    score = len(history) * 10

    if score > 100:
        score = 100

    return score


def generate_member_care_recommendations(member_name):
    history = get_member_ai_history(member_name, limit=10)

    recommendations = []

    if not history:
        recommendations.append(
            "No recent AI engagement found. Consider scheduling a pastoral follow-up."
        )
    else:
        titles = " ".join(
            item["title"] for item in history
        ).lower()

        if "birthday" in titles:
            recommendations.append(
                "Member has birthday engagement history. Consider personal follow-up and continued relationship building."
            )

        if "prayer" in titles:
            recommendations.append(
                "Member has prayer interaction history. Encourage spiritual growth and continued pastoral connection."
            )

        if "greeting" in titles:
            recommendations.append(
                "Member received personalized greeting. Maintain regular care communication."
            )

        if len(recommendations) == 0:
            recommendations.append(
                "Continue monitoring member engagement and encourage participation in ministry activities."
            )

    return recommendations

def get_ministry_care_statistics():
    from models import Member, ActivityLog

    total_members = Member.query.count()
    total_interactions = ActivityLog.query.count()

    average_care_score = 0

    if total_members:
        average_care_score = round(
            (total_interactions / total_members) * 10,
            2
        )

    return {
        "total_members": total_members,
        "total_interactions": total_interactions,
        "average_care_score": average_care_score
    }


def get_top_engaged_members(limit=5):
    from models import Member, ActivityLog
    from sqlalchemy import func

    results = (
        ActivityLog.query
        .join(Member, ActivityLog.details.contains(Member.full_name))
        .with_entities(
            Member.full_name,
            func.count(ActivityLog.id).label("interactions")
        )
        .group_by(Member.full_name)
        .order_by(func.count(ActivityLog.id).desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "name": row.full_name,
            "interactions": row.interactions
        }
        for row in results
    ]


def get_members_needing_attention(limit=5):
    from models import Member, ActivityLog
    from datetime import datetime

    members = Member.query.limit(limit).all()

    attention = []

    for member in members:
        last_activity = (
            ActivityLog.query
            .filter(
                ActivityLog.details.contains(member.full_name)
            )
            .order_by(ActivityLog.created_at.desc())
            .first()
        )

        if not last_activity:
            attention.append({
                "name": member.full_name,
                "reason": "No AI engagement history",
                "recommendation": "Schedule pastoral follow-up"
            })

    return attention
