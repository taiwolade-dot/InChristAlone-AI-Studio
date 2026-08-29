from extensions import mail
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from config import Config
from models import db, User
from modules.prompt_engine.routes import prompt_engine_bp

from modules.website_generator.routes import website_generator_bp
from modules.research_assistant.routes import research_assistant_bp

from modules.content_generator.routes import content_generator_bp

from modules.church_management.routes import church_management_bp
from modules.church_calendar.routes import church_calendar_bp

from modules.seminary_assistant.routes import seminary_assistant_bp

from modules.prompt_marketplace.routes import prompt_marketplace_bp

from modules.admin_panel.routes import admin_panel_bp
from modules.help_center.routes import help_center_bp
from modules.support.routes import support_bp
from modules.bible_quiz.routes import bible_quiz_bp
from modules.bible_quiz.session_routes import bible_quiz_session_bp
from modules.ai_assistant.routes import ai_assistant_bp

app = Flask(__name__)

app.config.from_object(Config)

mail.init_app(app)

db.init_app(app)
app.register_blueprint(prompt_engine_bp)
app.register_blueprint(website_generator_bp)
app.register_blueprint(research_assistant_bp)
app.register_blueprint(content_generator_bp)
app.register_blueprint(church_management_bp)
app.register_blueprint(church_calendar_bp)
app.register_blueprint(seminary_assistant_bp)
app.register_blueprint(prompt_marketplace_bp)
app.register_blueprint(admin_panel_bp)
app.register_blueprint(help_center_bp)
app.register_blueprint(support_bp)
app.register_blueprint(bible_quiz_bp)
app.register_blueprint(bible_quiz_session_bp)
app.register_blueprint(ai_assistant_bp)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --- Routes ---

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not password:
            flash('All fields are required.', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with that email already exists.', 'error')
            return redirect(url_for('register'))

        new_user = User(full_name=full_name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


with app.app_context():
    db.create_all()

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')


@app.route('/subscription')
@login_required
def subscription():
    return render_template('subscription.html')


@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', current_user.full_name)
        current_user.email = request.form.get('email', current_user.email).lower()

        db.session.commit()

        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html')



@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        old_password = request.form.get('old_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if not current_user.check_password(old_password):
            flash('Current password is incorrect.', 'error')
            return redirect(url_for('change_password'))

        if new_password != confirm_password:
            flash('New passwords do not match.', 'error')
            return redirect(url_for('change_password'))

        current_user.set_password(new_password)
        db.session.commit()

        flash('Password changed successfully.', 'success')
        return redirect(url_for('profile'))

    return render_template('change_password.html')




@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5000)