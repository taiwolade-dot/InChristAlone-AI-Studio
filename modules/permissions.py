from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if not current_user.is_authenticated:
                return redirect(url_for('login'))

            if current_user.role not in roles:
                flash('You do not have permission to access this feature.', 'error')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)

        return decorated_function
    return decorator
