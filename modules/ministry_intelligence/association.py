from collections import defaultdict

from models import ChurchProfile, PastorProfile


def association_summary():

    churches = ChurchProfile.query.all()

    associations = defaultdict(
        lambda: {
            "churches": 0,
            "pastors": 0
        }
    )

    for church in churches:
        name = church.association or "Not Assigned"

        associations[name]["churches"] += 1
        associations[name]["pastors"] += len(church.pastors)

    return dict(associations)


def conference_summary():

    churches = ChurchProfile.query.all()

    conferences = defaultdict(
        lambda: {
            "churches": 0,
            "associations": set()
        }
    )

    for church in churches:
        name = church.conference or "Not Assigned"

        conferences[name]["churches"] += 1

        if church.association:
            conferences[name]["associations"].add(
                church.association
            )

    for conference in conferences:
        conferences[conference]["associations"] = list(
            conferences[conference]["associations"]
        )

    return dict(conferences)


def generate_network_report():

    return {
        "associations": association_summary(),
        "conferences": conference_summary()
    }
