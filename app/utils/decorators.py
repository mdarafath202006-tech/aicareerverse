"""app/utils/decorators.py — Route protection decorators"""
from functools import wraps
from flask import session, redirect, url_for, flash, jsonify, request


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("user_id"):
            # JSON requests get 401
            if request.is_json or request.path.startswith("/api/"):
                return jsonify({"error": "Authentication required"}), 401
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if session.get("role") != role:
                if request.is_json or request.path.startswith("/api/"):
                    return jsonify({"error": "Forbidden"}), 403
                flash("Access denied.", "danger")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return decorated
    return decorator
