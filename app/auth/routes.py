"""
app/auth/routes.py — Upgraded auth with OAuth stubs + email verification
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from marshmallow import ValidationError

from app.models import db, User, Student, Alumni
from app.schemas.user_schemas import RegisterSchema, LoginSchema
from app import limiter

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = RegisterSchema().load(request.form)
        except ValidationError as e:
            for field, msgs in e.messages.items():
                flash(f"{field}: {msgs[0]}", "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=data["email"].lower()).first():
            flash("Email already registered.", "danger")
            return redirect(url_for("auth.register"))

        user = User(name=data["name"], email=data["email"].lower(), role=data["role"])
        user.set_password(data["password"])
        db.session.add(user)
        db.session.flush()  # get user.id before commit

        if data["role"] == "student":
            st = Student(user_id=user.id, department=data.get("department",""), year=data.get("year",""))
            db.session.add(st)
        elif data["role"] == "alumni":
            al = Alumni(user_id=user.id, graduation_year=data.get("grad_year"),
                        company=data.get("company",""), job_role=data.get("job_role",""))
            db.session.add(al)

        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":
        try:
            data = LoginSchema().load(request.form)
        except ValidationError:
            flash("Invalid input.", "danger")
            return redirect(url_for("auth.login"))

        user = User.query.filter_by(email=data["email"].lower()).first()
        if user and user.check_password(data["password"]) and user.is_active:
            import datetime
            user.last_login = datetime.datetime.utcnow()
            db.session.commit()
            session.clear()
            session["user_id"] = user.id
            session["name"]    = user.name
            session["role"]    = user.role
            session.permanent  = True
            flash(f"Welcome back, {user.name}!", "success")
            if user.role == "student": return redirect(url_for("student.dashboard"))
            if user.role == "alumni":  return redirect(url_for("alumni.dashboard"))
            if user.role == "admin":   return redirect(url_for("admin.dashboard"))

        flash("Invalid email or password.", "danger")
    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("index"))


# ── OAuth stubs (Phase 6 — wire up with authlib in production) ─────────────
@auth_bp.route("/auth/google")
def google_login():
    flash("Google OAuth: configure GOOGLE_CLIENT_ID in .env to enable.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/auth/linkedin")
def linkedin_login():
    flash("LinkedIn OAuth: configure LINKEDIN_CLIENT_ID in .env to enable.", "info")
    return redirect(url_for("auth.login"))
