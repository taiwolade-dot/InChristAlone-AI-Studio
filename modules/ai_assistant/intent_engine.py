def detect_module(question):

    q = question.lower()


    if any(word in q for word in [
        "programme",
        "program",
        "event",
        "calendar",
        "conference",
        "association",
        "convention"
    ]):
        return "calendar"


    if any(word in q for word in [
        "quiz",
        "bible quiz",
        "question",
        "competition"
    ]):
        return "quiz"


    if any(word in q for word in [
        "member",
        "membership",
        "birthday",
        "baptism"
    ]):
        return "members"


    if any(word in q for word in [
        "sermon",
        "preaching",
        "devotional"
    ]):
        return "content"


    if any(word in q for word in [
        "research",
        "thesis",
        "seminary",
        "academic"
    ]):
        return "seminary"


    return "general"
