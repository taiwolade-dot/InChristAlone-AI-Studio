def detect_event_type(
    title="",
    theme="",
    bible_verse=""
):

    text = (
        f"{title} {theme} {bible_verse}"
    ).lower()


    if any(word in text for word in [
        "revival",
        "crusade",
        "evangelism"
    ]):
        return "revival"

    if any(word in text for word in [
        "youth",
        "teen",
        "young"
    ]):
        return "youth"

    if any(word in text for word in [
        "conference",
        "convention",
        "assembly"
    ]):
        return "conference"

    if any(word in text for word in [
        "birthday",
        "celebration",
        "anniversary"
    ]):
        return "celebration"

    if any(word in text for word in [
        "training",
        "seminar",
        "workshop"
    ]):
        return "training"

    if any(word in text for word in [
        "prayer",
        "worship",
        "service"
    ]):
        return "worship"

    return "ministry"
