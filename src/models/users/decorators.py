from functools import wraps

from flask import session, url_for, request
from werkzeug.utils import redirect
from src.app import app


def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_users', next=request.path))
        return func(*args, **kwargs) #func(...) args: func(5, 6) kwargs: func(x=5, y=6)
    return decorated_function

def requires_admin_permissions(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_users', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_users'))
        return func(*args, **kwargs) #func(...) args: func(5, 6) kwargs: func(x=5, y=6)
    return decorated_function

