from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')
    wallet_balance = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, *roles):
        return self.role in roles

    def is_super_admin(self):
        return self.role == 'super_admin'

    def is_admin(self):
        return self.role in [
            'super_admin',
            'admin',
            'support_admin',
            'content_admin',
            'finance_admin'
        ]

    def __repr__(self):
        return f'<User {self.email}>'


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(30))
    email = db.Column(db.String(120))
    address = db.Column(db.String(255))
    church_role = db.Column(db.String(80))
    date_joined = db.Column(db.Date)
    date_of_salvation = db.Column(db.Date)
    date_of_baptism = db.Column(db.Date)
    marital_status = db.Column(db.String(30))
    age_range = db.Column(db.String(20))
    birthday = db.Column(db.Date)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Member {self.full_name}>'


class AcademicWork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_type = db.Column(db.String(30), nullable=False, default='thesis_chapter')
    title = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='not_started')
    deadline = db.Column(db.Date)
    notes = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    documents = db.relationship('AcademicDocument', backref='work', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<AcademicWork {self.title}>'


class AcademicDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    work_id = db.Column(db.Integer, db.ForeignKey('academic_work.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AcademicDocument {self.original_filename}>'


class PromptPack(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(80))
    price_units = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    pdf_filename = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<PromptPack {self.title}>'


class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pack_id = db.Column(db.Integer, db.ForeignKey('prompt_pack.id'), nullable=False)
    units_spent = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='purchases')
    pack = db.relationship('PromptPack', backref='purchases')

    def __repr__(self):
        return f'<Purchase user={self.user_id} pack={self.pack_id}>'


class WalletTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reference = db.Column(db.String(100), unique=True, nullable=False)
    amount_naira = db.Column(db.Integer, nullable=False)
    units_added = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='wallet_transactions')

    def __repr__(self):
        return f'<WalletTransaction {self.reference}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    admin_reply = db.Column(db.Text)
    status = db.Column(db.String(20), nullable=False, default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replied_at = db.Column(db.DateTime)

    user = db.relationship('User', backref='contact_messages')

    def __repr__(self):
        return f'<ContactMessage {self.subject}>'


import json
import random
import string


def gen_pin(length=6):
    return "".join(random.choices(string.digits, k=length))


class BibleQuiz(db.Model):
    __tablename__ = "quiz_quizzes"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    age_group = db.Column(db.String(20), default="Adults")
    source_type = db.Column(db.String(30))
    source_ref = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    questions = db.relationship(
        "QuizQuestion", backref="quiz", lazy=True, cascade="all, delete-orphan"
    )
    sessions = db.relationship(
        "QuizLiveSession",
        backref="quiz",
        lazy=True,
        cascade="all, delete-orphan"
    )


class QuizQuestion(db.Model):
    __tablename__ = "quiz_questions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz_quizzes.id"), nullable=False)
    text = db.Column(db.Text, nullable=False)
    options_json = db.Column(db.Text, nullable=False)
    correct_index = db.Column(db.Integer, nullable=False)
    scripture_ref = db.Column(db.String(150))
    explanation = db.Column(db.Text)
    difficulty = db.Column(db.String(10), default="Medium")
    order_index = db.Column(db.Integer, default=0)

    @property
    def options(self):
        return json.loads(self.options_json)

    @options.setter
    def options(self, value):
        self.options_json = json.dumps(value)


class QuizLiveSession(db.Model):
    __tablename__ = "quiz_sessions"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz_quizzes.id"), nullable=False)
    mode = db.Column(db.String(1), default="A")
    pin_code = db.Column(db.String(10), unique=True, default=gen_pin)
    status = db.Column(db.String(20), default="waiting")
    current_question_index = db.Column(db.Integer, default=0)
    question_started_at = db.Column(db.DateTime)
    seconds_per_question = db.Column(db.Integer, default=20)
    started_at = db.Column(db.DateTime)
    ended_at = db.Column(db.DateTime)

    participants = db.relationship(
        "QuizParticipant", backref="session", lazy=True, cascade="all, delete-orphan"
    )

    def participant_limit(self):
        return 12 if self.mode == "A" else 500


class QuizParticipant(db.Model):
    __tablename__ = "quiz_participants"

    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey("quiz_sessions.id"), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    avatar_color = db.Column(db.String(20), default="#d4af37")
    device_token = db.Column(db.String(64))
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)
    score = db.Column(db.Integer, default=0)

    answers = db.relationship(
        "QuizAnswer", backref="participant", lazy=True, cascade="all, delete-orphan"
    )


class QuizAnswer(db.Model):
    __tablename__ = "quiz_answers"

    id = db.Column(db.Integer, primary_key=True)
    participant_id = db.Column(db.Integer, db.ForeignKey("quiz_participants.id"), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("quiz_questions.id"), nullable=False)
    chosen_index = db.Column(db.Integer)
    is_correct = db.Column(db.Boolean, default=False)
    time_taken_ms = db.Column(db.Integer)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("participant_id", "question_id", name="uq_participant_question"),
    )


class ChurchEvent(db.Model):
    __tablename__ = "church_events"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)

    category = db.Column(
        db.String(50),
        default="Church"
    )

    level = db.Column(
        db.String(30),
        default="Local Church"
    )

    organization_name = db.Column(
        db.String(150),
        default="General"
    )

    ministry = db.Column(
        db.String(50),
        default="General"
    )

    description = db.Column(
        db.Text
    )

    venue = db.Column(
        db.String(200)
    )

    organizer = db.Column(
        db.String(150)
    )

    start_datetime = db.Column(
        db.DateTime,
        nullable=False
    )

    end_datetime = db.Column(
        db.DateTime
    )

    event_color = db.Column(
        db.String(20),
        default="#1a73e8"
    )

    is_public = db.Column(
        db.Boolean,
        default=True
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )



class AITransaction(db.Model):
    __tablename__ = "ai_transactions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    reference = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    amount_naira = db.Column(
        db.Integer,
        nullable=False
    )

    units = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )

    transaction_type = db.Column(
        db.String(50),
        default="recharge"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<AITransaction {self.reference}>"


class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    action = db.Column(
        db.String(200),
        nullable=False
    )

    module = db.Column(
        db.String(100),
        nullable=False
    )

    details = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="activity_logs"
    )

    def __repr__(self):
        return f"<ActivityLog {self.action}>"


class AIConversation(db.Model):
    __tablename__ = "ai_conversations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    module = db.Column(
        db.String(100),
        nullable=False
    )

    response = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        backref="ai_conversations"
    )

    def __repr__(self):
        return f"<AIConversation {self.module}>"
