from collections import Counter

from models import (
    ChurchProfile,
    ChurchEvent
)


def church_profile_comparison():

    churches = ChurchProfile.query.all()

    comparison = []

    for church in churches:
        comparison.append({
            "church_name": church.church_name,
            "association": church.association or "Not Assigned",
            "conference": church.conference or "Not Assigned",
            "pastors": len(church.pastors)
        })

    return comparison


def church_activity_comparison():

    events = ChurchEvent.query.all()

    activity = Counter()

    for event in events:
        if event.church_id:
            church = ChurchProfile.query.get(event.church_id)

            if church:
                activity[church.church_name] += 1

    return dict(activity)


def generate_comparative_report():

    return {
        "church_profiles": church_profile_comparison(),
        "church_activity": church_activity_comparison()
    }
