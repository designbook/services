"""
decorators.py

Decorators for URL handlers

"""

from functools import wraps
from google.appengine.api import users
from flask import redirect, request

from application.models import Project


def login_required(func):
    """Requires standard login credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.get_current_user():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view


def admin_required(func):
    """Requires App Engine admin credentials"""
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not users.is_current_user_admin():
            return redirect(users.create_login_url(request.url))
        return func(*args, **kwargs)
    return decorated_view

def project_required(f):
    """Requires a value project"""
    def decorator(*args, **kwargs):

        p = Project.get_by_id(kwargs['project_id'])
        if p is None:
            return "project not found", 404
        kwargs['project'] = p

        return f(*args, **kwargs)
    return decorator

