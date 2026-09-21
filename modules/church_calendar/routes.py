from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, ChurchEvent, ChurchProfile, PastorProfile
from sqlalchemy import or_
from datetime import datetime, timedelta


church_calendar_bp = Blueprint(
    "church_calendar",
    __name__,
    url_prefix="/church-calendar",
    template_folder="templates"
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

        church = ChurchProfile.query.filter_by(
            owner_id=current_user.id
        ).first()

        pastor = None

        if church:
            pastor = PastorProfile.query.filter_by(
                church_id=church.id
            ).first()


        event = ChurchEvent(
            title=request.form.get("title"),
            category=request.form.get("category"),
            level=request.form.get("level"),
            organization_name=request.form.get("organization_name"),
            ministry=request.form.get("ministry"),
            description=request.form.get("description"),
            venue=request.form.get("venue"),
            location=request.form.get("location"),
            association=request.form.get("association"),
            conference=request.form.get("conference"),
            convention=request.form.get("convention"),
            organizer=request.form.get("organizer"),
            start_datetime=datetime.fromisoformat(
                request.form.get("start_datetime")
            ),
            church_id=church.id if church else None,
            pastor_id=pastor.id if pastor else None,
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



@church_calendar_bp.route("/dashboard")
@login_required
def dashboard():

    now = datetime.utcnow()

    total_events = ChurchEvent.query.count()

    upcoming_events = ChurchEvent.query.filter(
        ChurchEvent.start_datetime >= now
    ).order_by(
        ChurchEvent.start_datetime.asc()
    ).limit(10).all()


    month_events = ChurchEvent.query.filter(
        db.extract(
            "month",
            ChurchEvent.start_datetime
        ) == now.month
    ).count()


    year_events = ChurchEvent.query.filter(
        db.extract(
            "year",
            ChurchEvent.start_datetime
        ) == now.year
    ).count()


    ministry_stats = {}

    for ministry in [
        "Youth",
        "WMU",
        "MMU",
        "General"
    ]:
        ministry_stats[ministry] = ChurchEvent.query.filter(
            ChurchEvent.ministry == ministry
        ).count()


    level_stats = {}

    for level in [
        "Local Church",
        "Association",
        "Conference",
        "Convention"
    ]:
        level_stats[level] = ChurchEvent.query.filter(
            ChurchEvent.level == level
        ).count()


    monthly_stats = {}

    for month in range(1, 13):
        monthly_stats[month] = ChurchEvent.query.filter(
            db.extract(
                "month",
                ChurchEvent.start_datetime
            ) == month
        ).count()


    for event in upcoming_events:
        event.days_remaining = (event.start_datetime - now).days


    total_upcoming = len(upcoming_events)


    busiest_month = max(
        monthly_stats,
        key=monthly_stats.get
    )


    active_ministry = max(
        ministry_stats,
        key=ministry_stats.get
    )


    active_level = max(
        level_stats,
        key=level_stats.get
    )


    next_7_days = now + timedelta(days=7)

    next_30_days = now + timedelta(days=30)


    events_next_7_days = ChurchEvent.query.filter(
        ChurchEvent.start_datetime >= now,
        ChurchEvent.start_datetime <= next_7_days
    ).count()


    events_next_30_days = ChurchEvent.query.filter(
        ChurchEvent.start_datetime >= now,
        ChurchEvent.start_datetime <= next_30_days
    ).count()


    completed_events = ChurchEvent.query.filter(
        ChurchEvent.start_datetime < now
    ).count()


    completed_recent_events = ChurchEvent.query.filter(
        ChurchEvent.start_datetime < now
    ).order_by(
        ChurchEvent.start_datetime.desc()
    ).limit(5).all()


    average_monthly_events = round(
        year_events / 12,
        1
    )


    return render_template(
        "church_calendar/dashboard.html",
        total_events=total_events,
        upcoming_events=upcoming_events,
        month_events=month_events,
        year_events=year_events,
        ministry_stats=ministry_stats,
        level_stats=level_stats,
        monthly_stats=monthly_stats,
        total_upcoming=total_upcoming,
        busiest_month=busiest_month,
        active_ministry=active_ministry,
        active_level=active_level,
        events_next_7_days=events_next_7_days,
        events_next_30_days=events_next_30_days,
        completed_events=completed_events,
        average_monthly_events=average_monthly_events,
        completed_recent_events=completed_recent_events
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


        # Ministry Intelligence

        ministries = [
            "youth",
            "wmu",
            "mmu"
        ]

        for ministry in ministries:
            if ministry in question:
                query = query.filter(
                    ChurchEvent.ministry.ilike(f"%{ministry}%")
                )


        # Organization Level Intelligence

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


        # Location Intelligence

        words = question.split()

        for word in words:
            if len(word) > 3:
                query = query.filter(
                    or_(
                        ChurchEvent.location.ilike(f"%{word}%"),
                        ChurchEvent.venue.ilike(f"%{word}%")
                    )
                )


        # Association / Conference / Convention names

        query = query.filter(
            or_(
                ChurchEvent.association.ilike(f"%{question}%"),
                ChurchEvent.conference.ilike(f"%{question}%"),
                ChurchEvent.convention.ilike(f"%{question}%")
            )
        ) if any(
            x in question for x in [
                "association",
                "conference",
                "convention"
            ]
        ) else query


        # Year Intelligence

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


        # Quarter Intelligence

        quarters = {
            "q1": (1,3),
            "q2": (4,6),
            "q3": (7,9),
            "q4": (10,12)
        }

        for key, months in quarters.items():

            if key in question:

                query = query.filter(
                    db.extract(
                        "month",
                        ChurchEvent.start_datetime
                    ) >= months[0],
                    db.extract(
                        "month",
                        ChurchEvent.start_datetime
                    ) <= months[1]
                )


        events = query.order_by(
            ChurchEvent.start_datetime.asc()
        ).all()


    return render_template(
        "church_calendar/ai_search.html",
        events=events
    )
