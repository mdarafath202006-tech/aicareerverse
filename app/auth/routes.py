"""
app/auth/routes.py — Auth Blueprint V3
Login, register, logout, OAuth stubs.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models import db, User, Student, Alumni
from app import limiter

auth_bp = Blueprint("auth", __name__)


def _validate_password(password: str) -> str | None:
    """Return error string or None if valid."""
    if len(password) < 8:
        return "Password must be at least 8 characters."
    if not any(c.isupper() for c in password):
        return "Password must contain at least one uppercase letter."
    if not any(c.isdigit() for c in password):
        return "Password must contain at least one digit."
    return None


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("index"))

    if request.method == "POST":
        name     = (request.form.get("name")     or "").strip()[:100]
        email    = (request.form.get("email")    or "").strip().lower()[:150]
        password = (request.form.get("password") or "")
        role     = (request.form.get("role")     or "student")

        if not name or not email or not password:
            flash("All fields are required.", "danger")
            return redirect(url_for("auth.register"))
        if role not in ("student", "alumni"):
            flash("Invalid role.", "danger")
            return redirect(url_for("auth.register"))

        pw_err = _validate_password(password)
        if pw_err:
            flash(pw_err, "danger")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(email=email).first():
            flash("Email already registered. Please sign in.", "danger")
            return redirect(url_for("auth.register"))

        user = User(name=name, email=email, role=role, is_active=True,
                    email_verified=False)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        if role == "student":
            st = Student(
                user_id=user.id,
                department=(request.form.get("department") or "")[:100],
                year=(request.form.get("year") or "")[:20],
                skills=(request.form.get("skills") or "")[:500],
            )
            db.session.add(st)
        elif role == "alumni":
            al = Alumni(
                user_id=user.id,
                company=(request.form.get("company") or "")[:150],
                job_role=(request.form.get("job_role") or "")[:150],
                skills=(request.form.get("skills") or "")[:500],
            )
            try:
                al.graduation_year = int(request.form.get("grad_year") or 0) or None
            except (ValueError, TypeError):
                pass
            db.session.add(al)

        db.session.commit()
        flash(f"Welcome to AI CareerVerse, {name}! 🎉 Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
@limiter.limit("10 per minute")
def login():
    if session.get("user_id"):
        role = session.get("role")
        if role == "student": return redirect(url_for("student.dashboard"))
        if role == "alumni":  return redirect(url_for("alumni.dashboard"))
        if role == "admin":   return redirect(url_for("admin.dashboard"))

    if request.method == "POST":
        email    = (request.form.get("email")    or "").strip().lower()
        password = (request.form.get("password") or "")
        user     = User.query.filter_by(email=email).first()

        if user and user.check_password(password) and user.is_active:
            import datetime
            user.last_login = datetime.datetime.utcnow()
            db.session.commit()
            session.clear()
            session["user_id"]  = user.id
            session["name"]     = user.name
            session["role"]     = user.role
            session.permanent   = True
            flash(f"Welcome back, {user.name}! 👋", "success")
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            if user.role == "student": return redirect(url_for("student.dashboard"))
            if user.role == "alumni":  return redirect(url_for("alumni.dashboard"))
            if user.role == "admin":   return redirect(url_for("admin.dashboard"))

        flash("Invalid email or password. Please try again.", "danger")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    name = session.get("name", "")
    session.clear()
    flash(f"Goodbye{', ' + name if name else ''}! See you soon.", "info")
    return redirect(url_for("index"))


# ── OAuth stubs (configure via .env to enable) ────────────────────────────────
@auth_bp.route("/auth/google")
def google_login():
    flash("Google OAuth: add GOOGLE_CLIENT_ID & GOOGLE_CLIENT_SECRET in .env.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/auth/linkedin")
def linkedin_login():
    flash("LinkedIn OAuth: add LINKEDIN_CLIENT_ID & LINKEDIN_CLIENT_SECRET in .env.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/auth/github")
def github_login():
    flash("GitHub OAuth coming soon!", "info")
    return redirect(url_for("auth.login"))
