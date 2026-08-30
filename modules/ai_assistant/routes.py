from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import ChurchEvent, db, BibleQuiz, Member, AcademicWork, AcademicDocument, AIConversation
from datetime import datetime
from modules.content_generator.data import CONTENT_TYPES
from .intent_engine import detect_module
from modules.ai_service import ask_ai


ai_assistant_bp = Blueprint(
    "ai_assistant",
    __name__,
    url_prefix="/ai"
)



def search_calendar(question):

    q = question.lower()

    query = ChurchEvent.query


    if "association" in q:
        query = query.filter(
            ChurchEvent.level == "Association"
        )

    elif "conference" in q:
        query = query.filter(
            ChurchEvent.level == "Conference"
        )

    elif "convention" in q:
        query = query.filter(
            ChurchEvent.level == "Convention"
        )


    if "youth" in q:
        query = query.filter(
            ChurchEvent.ministry == "Youth"
        )


    organization_map = {
        "nbc": "Nigerian Baptist Convention",
        "nba": "Nazareth Baptist Association",
        "fctbc": "FCT Baptist Conference",
        "fct baptist conference": "FCT Baptist Conference",
        "vbc": "Victory Baptist Church",
        "general": "General"
    }


    for keyword, org_name in organization_map.items():
        if keyword in q:
            query = query.filter(
                ChurchEvent.organization_name.ilike(
                    f"%{org_name}%"
                )
            )
            break


    for org in organization_map.values():
        if org in q:
            query = query.filter(
                ChurchEvent.organization_name.ilike(
                    f"%{org}%"
                )
            )
            break


    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }


    for month_name, month_number in months.items():
        if month_name in q:
            query = query.filter(
                db.extract(
                    "month",
                    ChurchEvent.start_datetime
                ) == month_number
            )
            break


    quarters = {
        "q1": (1, 3),
        "q2": (4, 6),
        "q3": (7, 9),
        "q4": (10, 12)
    }


    for quarter, (start_month, end_month) in quarters.items():
        if quarter in q:
            query = query.filter(
                db.extract(
                    "month",
                    ChurchEvent.start_datetime
                ).between(start_month, end_month)
            )
            break


    if "first half" in q or "h1" in q:
        query = query.filter(
            db.extract(
                "month",
                ChurchEvent.start_datetime
            ).between(1, 6)
        )


    if "second half" in q or "h2" in q:
        query = query.filter(
            db.extract(
                "month",
                ChurchEvent.start_datetime
            ).between(7, 12)
        )


    events = query.order_by(
        ChurchEvent.start_datetime.asc()
    ).limit(10).all()


    if not events:
        return "No matching programmes found."


    result = "📅 Programmes Found:\n\n"

    for event in events:
        result += (
            f"• {event.title}\n"
            f"  {event.organization_name}\n"
            f"  {event.start_datetime}\n"
            f"  {event.venue}\n\n"
        )

    return result






def generate_content(question):

    q = question.lower()


    if "flyer" in q or "poster" in q:
        content_type = "flyer"

    elif "video" in q or "script" in q:
        content_type = "video"

    elif "song" in q or "music" in q or "worship" in q:
        content_type = "music"

    else:
        content_type = "cartoon"


    template = CONTENT_TYPES.get(content_type)


    return (
        f"✍ Content Type: {template['label']}\n\n"
        "Your request has been identified for content generation.\n\n"
        f"Prompt Framework:\n{template['template']}"
    )


def search_seminary(question):

    q = question.lower()


    if "document" in q or "file" in q:

        documents = AcademicDocument.query.limit(10).all()

        if not documents:
            return "No academic documents found."


        result = "📄 Academic Documents:\n\n"

        for doc in documents:
            result += (
                f"• {doc.original_filename}\n"
            )

        return result


    works = AcademicWork.query.order_by(
        AcademicWork.created_at.desc()
    ).limit(10).all()


    if not works:
        return "No academic works found."


    result = "🎓 Academic Works:\n\n"

    for work in works:
        result += (
            f"• {work.title}\n"
            f"  Status: {work.status}\n"
            f"  Type: {work.work_type}\n\n"
        )

    return result


def search_members(question):

    q = question.lower()

    if "baptized" in q or "baptism" in q:
        count = Member.query.filter(
            Member.date_of_baptism.isnot(None)
        ).count()

        return (
            f"💧 Baptized Members: {count}"
        )


    # Name search
    words = q.split()

    ignored = [
        "find",
        "search",
        "show",
        "member",
        "members",
        "with",
        "name"
    ]

    search_terms = [
        word for word in words
        if word not in ignored
    ]


    if search_terms:

        for term in search_terms:

            members = Member.query.filter(
                Member.full_name.ilike(
                    f"%{term}%"
                )
            ).all()

            if members:

                result = "👥 Members Found:\n\n"

                for member in members:
                    result += (
                        f"• {member.full_name}\n"
                        f"  Role: {member.church_role}\n"
                        f"  Phone: {member.phone}\n\n"
                    )

                return result


    roles = [
        "pastor",
        "deacon",
        "leader",
        "worker"
    ]


    for role in roles:
        if role in q:

            members = Member.query.filter(
                Member.church_role.ilike(
                    f"%{role}%"
                )
            ).all()

            if not members:
                return f"No members found with role: {role}"


            result = f"👥 {role.title()}s Found:\n\n"

            for member in members:
                result += (
                    f"• {member.full_name}\n"
                    f"  Role: {member.church_role}\n\n"
                )

            return result


    if "how many" in q or "count" in q:
        count = Member.query.count()

        return (
            f"👥 Total Members: {count}"
        )


    months = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12
    }


    for month_name, month_number in months.items():
        if month_name in q:
            members = Member.query.filter(
                db.extract(
                    "month",
                    Member.birthday
                ) == month_number
            ).all()

            if not members:
                return "No members found for that birthday month."

            result = "🎂 Birthday Members:\n\n"

            for member in members:
                result += (
                    f"• {member.full_name}\n"
                    f"  Birthday: {member.birthday}\n\n"
                )

            return result


    members = Member.query.order_by(
        Member.full_name.asc()
    ).limit(10).all()


    if not members:
        return "No members found."


    result = "👥 Members Found:\n\n"

    for member in members:
        result += (
            f"• {member.full_name}\n"
            f"  Role: {member.church_role}\n"
            f"  Phone: {member.phone}\n\n"
        )

    return result


def search_bible_quiz():

    quizzes = BibleQuiz.query.order_by(
        BibleQuiz.created_at.desc()
    ).limit(10).all()


    if not quizzes:
        return "No Bible quizzes found."


    result = "📖 Bible Quizzes:\n\n"

    for quiz in quizzes:
        result += (
            f"• {quiz.title}\n"
            f"  Age Group: {quiz.age_group}\n"
            f"  Questions: {len(quiz.questions)}\n\n"
        )

    return result


@ai_assistant_bp.route("/", methods=["GET", "POST"])
@login_required
def chat():

    answer = ""

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        )


        module = detect_module(
            question
        )


        if module == "quiz":
            title = "📖 Bible Quiz"
            response = search_bible_quiz()


        elif module == "calendar":
            title = "📅 Church Calendar"
            response = search_calendar(question)


        elif module == "members":
            title = "👥 Church Management"
            response = search_members(question)


        elif module == "seminary":
            title = "🎓 Seminary Assistant"
            response = search_seminary(question)


        elif module == "content":
            title = "✍ Content Generator"
            response = generate_content(question)


        elif module == "sermon":
            title = "🎤 Sermon Assistant"
            response = ask_ai(question)

        elif module == "prayer":
            title = "🙏 Prayer Assistant"
            response = ask_ai(question)

        elif module == "worship":
            title = "🎶 Worship Assistant"
            response = ask_ai(question)

        elif module == "ai_help":
            title = "🤖 AI Studio Help"
            response = ask_ai(question)

        else:
            title = "🤖 AI Assistant"
            response = ask_ai(question)



        answer = f"""
{title}

{response}

Your request:
{question}
"""



        conversation = AIConversation(
            user_id=current_user.id,
            question=question,
            module=module,
            response=response
        )

        db.session.add(conversation)
        db.session.commit()

    return render_template(
        "ai_assistant/chat.html",
        answer=answer
    )
