from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, ChurchEvent
from sqlalchemy import or_
from datetime import datetime


church_calendar_bp = Blueprint(
    "church_calendar",
    __name__,
    url_prefix="/church-calendar"
)


@church_calendar_bp.route("/")
@login_required
def index():

    query = ChurchEvent.query

    keyword = request.args.get("keyword", "")
    level = request.args.get("level", "")
    ministry = request.args.get("ministry", "")
    period = request.args.get("period", "")
    year = request.args.get("year", "")

    if keyword:
        query = query.filter(
            or_(
                ChurchEvent.title.ilike(f"%{keyword}%"),
                ChurchEvent.description.ilike(f"%{keyword}%"),
                ChurchEvent.organization_name.ilike(f"%{keyword}%")
            )
        )

    if level:
        query = query.filter(
            ChurchEvent.level == level
        )

    if ministry:
        query = query.filter(
            ChurchEvent.ministry == ministry
        )

    if year:
        query = query.filter(
            db.extract("year", ChurchEvent.start_datetime) == int(year)
        )

    if period:
        ranges = {
            "q1": (1, 3),
            "q2": (4, 6),
            "q3": (7, 9),
            "q4": (10, 12),
            "h1": (1, 6),
            "h2": (7, 12)
        }

        if period in ranges:
            start, end = ranges[period]

            query = query.filter(
                db.extract("month", ChurchEvent.start_datetime) >= start,
                db.extract("month", ChurchEvent.start_datetime) <= end
            )

    events = query.order_by(
        ChurchEvent.start_datetime.asc()
    ).all()

    return render_template(
        "church_calendar/index.html",
        events=events
    )


@church_calendar_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_event():

    if request.method == "POST":

        event = ChurchEvent(
            title=request.form.get("title"),
            category=request.form.get("category"),
            level=request.form.get("level"),
            organization_name=request.form.get("organization_name"),
            ministry=request.form.get("ministry"),
            description=request.form.get("description"),
            venue=request.form.get("venue"),
            organizer=request.form.get("organizer"),
            start_datetime=datetime.fromisoformat(
                request.form.get("start_datetime")
            ),
            created_by=current_user.id
        )

        db.session.add(event)
        db.session.commit()

        flash("Church event added successfully.", "success")

        return redirect(
            url_for("church_calendar.index")
        )


    return render_template(
        "church_calendar/new_event.html"
    )


@church_calendar_bp.route("/print")
@login_required
def print_calendar():

    query = ChurchEvent.query

    keyword = request.args.get("keyword", "")
    level = request.args.get("level", "")
    ministry = request.args.get("ministry", "")
    year = request.args.get("year", "")

    if keyword:
        query = query.filter(
            or_(
                ChurchEvent.title.ilike(f"%{keyword}%"),
                ChurchEvent.description.ilike(f"%{keyword}%"),
                ChurchEvent.organization_name.ilike(f"%{keyword}%")
            )
        )

    if level:
        query = query.filter(
            ChurchEvent.level == level
        )

    if ministry:
        query = query.filter(
            ChurchEvent.ministry == ministry
        )

    if year:
        query = query.filter(
            db.extract("year", ChurchEvent.start_datetime) == int(year)
        )

    events = query.order_by(
        ChurchEvent.start_datetime.asc()
    ).all()

    return render_template(
        "church_calendar/print.html",
        events=events
    )


@church_calendar_bp.route("/pdf")
@login_required
def calendar_pdf():

    from flask import send_file
    from io import BytesIO
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    query = ChurchEvent.query

    keyword = request.args.get("keyword", "")
    level = request.args.get("level", "")
    ministry = request.args.get("ministry", "")
    year = request.args.get("year", "")

    if keyword:
        query = query.filter(
            or_(
                ChurchEvent.title.ilike(f"%{keyword}%"),
                ChurchEvent.description.ilike(f"%{keyword}%"),
                ChurchEvent.organization_name.ilike(f"%{keyword}%")
            )
        )

    if level:
        query = query.filter(
            ChurchEvent.level == level
        )

    if ministry:
        query = query.filter(
            ChurchEvent.ministry == ministry
        )

    if year:
        query = query.filter(
            db.extract("year", ChurchEvent.start_datetime) == int(year)
        )

    events = query.order_by(
        ChurchEvent.start_datetime.asc()
    ).all()

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Church Calendar Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    for event in events:

        text = f"""
        <b>{event.title}</b><br/>
        Organization: {event.organization_name}<br/>
        Level: {event.level}<br/>
        Ministry: {event.ministry}<br/>
        Date: {event.start_datetime}<br/>
        Venue: {event.venue}<br/>
        Description: {event.description or ''}
        """

        content.append(
            Paragraph(text, styles["Normal"])
        )

        content.append(
            Spacer(1, 15)
        )

    doc.build(content)

    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name="Church_Calendar_Report.pdf",
        mimetype="application/pdf"
    )


@church_calendar_bp.route("/ai", methods=["GET", "POST"])
@login_required
def ai_calendar():

    events = []

    if request.method == "POST":

        question = request.form.get(
            "question",
            ""
        ).lower()


        query = ChurchEvent.query


        if "youth" in question:
            query = query.filter(
                ChurchEvent.ministry == "Youth"
            )

        elif "wmu" in question:
            query = query.filter(
                ChurchEvent.ministry == "WMU"
            )

        elif "mmu" in question:
            query = query.filter(
                ChurchEvent.ministry == "MMU"
            )


        if "association" in question:
            query = query.filter(
                ChurchEvent.level == "Association"
            )

        elif "conference" in question:
            query = query.filter(
                ChurchEvent.level == "Conference"
            )

        elif "convention" in question:
            query = query.filter(
                ChurchEvent.level == "Convention"
            )


        import re

        year_match = re.search(
            r"20\d{2}",
            question
        )

        if year_match:

            year = int(
                year_match.group()
            )

            query = query.filter(
                db.extract(
                    "year",
                    ChurchEvent.start_datetime
                ) == year
            )


        events = query.order_by(
            ChurchEvent.start_datetime.asc()
        ).all()


    return render_template(
        "church_calendar/ai_search.html",
        events=events
    )
