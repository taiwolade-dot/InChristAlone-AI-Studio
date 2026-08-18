import secrets
import qrcode
import io
import base64
from datetime import datetime, timedelta

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session as flask_session
from flask_login import login_required, current_user

from models import db, BibleQuiz, QuizLiveSession, QuizParticipant, QuizQuestion, QuizAnswer
from modules.bible_quiz.timer import seconds_remaining


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        box_size=8,
        border=2
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return encoded


bible_quiz_session_bp = Blueprint(
    'bible_quiz_session',
    __name__,
    template_folder='../../templates/bible_quiz'
)


@bible_quiz_session_bp.route('/bible-quiz/<int:quiz_id>/start', methods=['GET', 'POST'])
@login_required
def start_session(quiz_id):
    quiz = BibleQuiz.query.filter_by(id=quiz_id, owner_id=current_user.id).first_or_404()

    if request.method == 'POST':
        mode = request.form.get('mode', 'A')
        seconds = int(request.form.get('seconds_per_question', 20))

        quiz_session = QuizLiveSession(
            quiz_id=quiz.id, mode=mode, seconds_per_question=seconds, status='waiting'
        )
        db.session.add(quiz_session)
        db.session.commit()

        return redirect(url_for('bible_quiz_session.host_panel', session_id=quiz_session.id))

    return render_template('bible_quiz/start_session.html', quiz=quiz)


@bible_quiz_session_bp.route('/bible-quiz/host/<int:session_id>')
@login_required
def host_panel(session_id):
    quiz_session = QuizLiveSession.query.get_or_404(session_id)
    return render_template('bible_quiz/host_panel.html', quiz_session=quiz_session)


@bible_quiz_session_bp.route('/bible-quiz/dashboard/<int:session_id>')
def projector_dashboard(session_id):
    quiz_session = QuizLiveSession.query.get_or_404(session_id)

    join_url = request.host_url.rstrip('/') + url_for(
        'bible_quiz_session.join',
        pin_code=quiz_session.pin_code
    )

    qr_code = generate_qr_code(join_url)

    return render_template(
        'bible_quiz/projector_dashboard.html',
        quiz_session=quiz_session,
        qr_code=qr_code,
        join_url=join_url
    )


@bible_quiz_session_bp.route('/bible-quiz/join/<pin_code>', methods=['GET', 'POST'])
def join(pin_code):
    quiz_session = QuizLiveSession.query.filter_by(pin_code=pin_code).first_or_404()

    if quiz_session.status not in ('waiting', 'active'):
        flash('This quiz session has already ended.', 'error')
        return redirect(url_for('bible_quiz_session.join_landing'))

    current_count = len(quiz_session.participants)
    if current_count >= quiz_session.participant_limit():
        flash('This session is full.', 'error')
        return redirect(url_for('bible_quiz_session.join_landing'))

    if request.method == 'POST':
        name = request.form['name'].strip()[:80]
        avatar_color = request.form.get('avatar_color', '#d4af37')

        device_token = secrets.token_hex(16)
        participant = QuizParticipant(
            session_id=quiz_session.id,
            name=name,
            avatar_color=avatar_color,
            device_token=device_token,
        )
        db.session.add(participant)
        db.session.commit()

        flask_session['participant_id'] = participant.id
        flask_session['device_token'] = device_token

        return redirect(url_for('bible_quiz_session.play', session_id=quiz_session.id))

    return render_template('bible_quiz/join.html', quiz_session=quiz_session)


@bible_quiz_session_bp.route('/bible-quiz/join', methods=['GET', 'POST'])
def join_landing():
    if request.method == 'POST':
        pin_code = request.form['pin_code'].strip()
        return redirect(url_for('bible_quiz_session.join', pin_code=pin_code))
    return render_template('bible_quiz/join_landing.html')


@bible_quiz_session_bp.route('/bible-quiz/play/<int:session_id>')
def play(session_id):
    participant_id = flask_session.get('participant_id')
    if not participant_id:
        return redirect(url_for('bible_quiz_session.join_landing'))

    quiz_session = QuizLiveSession.query.get_or_404(session_id)
    participant = QuizParticipant.query.get_or_404(participant_id)

    return render_template('bible_quiz/play.html', quiz_session=quiz_session, participant=participant)


def _leaderboard_payload(quiz_session):
    participants = sorted(quiz_session.participants, key=lambda p: p.score, reverse=True)
    return [
        {'id': p.id, 'name': p.name, 'score': p.score, 'avatar_color': p.avatar_color}
        for p in participants
    ]



@bible_quiz_session_bp.route('/api/bible-quiz/session/<int:session_id>/state')
def api_session_state(session_id):
    quiz_session = QuizLiveSession.query.get_or_404(session_id)
    questions = sorted(quiz_session.quiz.questions,key=lambda q:q.order_index)

    if quiz_session.status=="active" and quiz_session.current_question_index < len(questions):

        if seconds_remaining(quiz_session)<=0:

            quiz_session.current_question_index += 1

            if quiz_session.current_question_index >= len(questions):
                quiz_session.status="finished"
                quiz_session.ended_at=datetime.utcnow()
            else:
                quiz_session.question_started_at=datetime.utcnow()

            db.session.commit()

            questions = sorted(quiz_session.quiz.questions,key=lambda q:q.order_index)

    payload={
        "status":quiz_session.status,
        "current_question_index":quiz_session.current_question_index,
        "total_questions":len(questions),
        "leaderboard":_leaderboard_payload(quiz_session)
    }

    if quiz_session.current_question_index < len(questions):
        q=questions[quiz_session.current_question_index]
        payload["question"]={
            "question_id":q.id,
            "text":q.text,
            "options":q.options,
            "seconds":seconds_remaining(quiz_session),
            "correct_index":q.correct_index if seconds_remaining(quiz_session)<=0 else None
        }

    return jsonify(payload)


@bible_quiz_session_bp.route('/bible-quiz/session/<int:session_id>/start-quiz', methods=['POST'])
@login_required
def api_start_quiz(session_id):
    quiz_session = QuizLiveSession.query.get_or_404(session_id)
    quiz_session.status = 'active'
    quiz_session.current_question_index = 0
    quiz_session.started_at = datetime.utcnow()
    quiz_session.question_started_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'ok': True})


@bible_quiz_session_bp.route('/bible-quiz/session/<int:session_id>/next-question', methods=['POST'])
def api_next_question(session_id):
    quiz_session = QuizLiveSession.query.get_or_404(session_id)
    questions = sorted(quiz_session.quiz.questions, key=lambda q: q.order_index)
    quiz_session.current_question_index += 1

    if quiz_session.current_question_index >= len(questions):
        quiz_session.status = 'finished'
        quiz_session.ended_at = datetime.utcnow()
        db.session.commit()
        return jsonify({'ok': True, 'finished': True})

    quiz_session.question_started_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'ok': True, 'finished': False})



@bible_quiz_session_bp.route('/bible-quiz/session/<int:session_id>/auto-advance', methods=['POST'])
def auto_advance(session_id):
    quiz_session = QuizLiveSession.query.get_or_404(session_id)

    # Only active sessions can advance
    if quiz_session.status != "active":
        return jsonify({"advanced": False, "status": quiz_session.status})

    questions = sorted(
        quiz_session.quiz.questions,
        key=lambda q: q.order_index
    )

    # No more questions
    if quiz_session.current_question_index >= len(questions):
        quiz_session.status = "finished"
        quiz_session.ended_at = datetime.utcnow()
        db.session.commit()
        return jsonify({"advanced": False, "finished": True})

    question = questions[quiz_session.current_question_index]

    total_players = QuizParticipant.query.filter_by(
        session_id=session_id
    ).count()

    answered = QuizAnswer.query.filter_by(
        question_id=question.id
    ).count()

    time_up = seconds_remaining(quiz_session) <= -5
    everyone_answered = (
        total_players > 0 and answered >= total_players
    )

    # Advance exactly when everyone has answered OR time has expired
    if not time_up and not everyone_answered:
        return jsonify({
            "advanced": False,
            "seconds": seconds_remaining(quiz_session),
            "answered": answered,
            "players": total_players
        })

    quiz_session.current_question_index += 1

    if quiz_session.current_question_index >= len(questions):
        quiz_session.status = "finished"
        quiz_session.ended_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "advanced": True,
            "finished": True
        })

    # Start the new question timer
    quiz_session.question_started_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        "advanced": True,
        "finished": False,
        "current_question_index": quiz_session.current_question_index
    })


@bible_quiz_session_bp.route('/bible-quiz/session/<int:session_id>/pause', methods=['POST'])
@login_required
def api_pause(session_id):
    quiz_session = QuizLiveSession.query.get_or_404(session_id)
    quiz_session.status = 'paused'
    db.session.commit()
    return jsonify({'ok': True})


@bible_quiz_session_bp.route('/bible-quiz/session/<int:session_id>/answer', methods=['POST'])
def api_submit_answer(session_id):
    participant_id = flask_session.get('participant_id')
    if not participant_id:
        return jsonify({'error': 'not_joined'}), 403

    data = request.get_json()
    chosen_index = data.get('chosen_index')
    time_taken_ms = data.get('time_taken_ms', 0)

    quiz_session = QuizLiveSession.query.get_or_404(session_id)
    questions = sorted(quiz_session.quiz.questions, key=lambda q: q.order_index)
    question = questions[quiz_session.current_question_index]

    existing = QuizAnswer.query.filter_by(
        participant_id=participant_id, question_id=question.id
    ).first()
    if existing:
        return jsonify({'already_answered': True})

    is_correct = int(chosen_index) == question.correct_index
    answer = QuizAnswer(
        participant_id=participant_id,
        question_id=question.id,
        chosen_index=chosen_index,
        is_correct=is_correct,
        time_taken_ms=time_taken_ms,
    )
    db.session.add(answer)

    participant = QuizParticipant.query.get(participant_id)
    if is_correct:
        base_points = 100
        speed_bonus = max(0, 20 - int(time_taken_ms / 1000))
        participant.score += base_points + speed_bonus

    db.session.commit()

    return jsonify({'is_correct': is_correct, 'correct_index': question.correct_index, 'score': participant.score})




@bible_quiz_session_bp.route('/api/bible-quiz/session/<int:session_id>/players')
def api_players(session_id):

    quiz_session = QuizLiveSession.query.get_or_404(session_id)

    players = [
        {
            "id": p.id,
            "name": p.name,
            "score": p.score,
            "avatar_color": p.avatar_color
        }
        for p in quiz_session.participants
    ]

    return jsonify({
        "count": len(players),
        "players": players
    })
