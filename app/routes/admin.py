"""app/routes/admin.py — Admin blueprint (SQLAlchemy)"""
from flask import Blueprint, render_template, session, redirect, url_for, flash, request, jsonify
from app.utils.decorators import login_required, role_required
from app.models import db, User, Student, Alumni, MentorshipRequest

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    user_count   = User.query.count()
    student_count = User.query.filter_by(role="student").count()
    alumni_count  = User.query.filter_by(role="alumni").count()
    req_count     = MentorshipRequest.query.count()
    recent_users  = User.query.order_by(User.created_at.desc()).limit(10).all()
    return render_template("admin/dashboard.html",
                           user_count=user_count, student_count=student_count,
                           alumni_count=alumni_count, req_count=req_count,
                           recent_users=recent_users)


@admin_bp.route("/users")
@login_required
@role_required("admin")
def users():
    page  = request.args.get("page", 1, type=int)
    users = User.query.order_by(User.created_at.desc()).paginate(page=page, per_page=20)
    return render_template("admin/users.html", users=users)


@admin_bp.route("/users/<int:uid>/toggle", methods=["POST"])
@login_required
@role_required("admin")
def toggle_user(uid):
    user = User.query.get_or_404(uid)
    user.is_active = not user.is_active
    db.session.commit()
    return jsonify({"active": user.is_active})


@admin_bp.route("/stats")
@login_required
@role_required("admin")
def stats():
    from app.ai.recommender import get_career_analytics
    alumni_data = [
        {"job_role": a.job_role, "company": a.company,
         "skills": a.skills, "graduation_year": a.graduation_year}
        for a in Alumni.query.all()
    ]
    data = get_career_analytics(alumni_data)
    return jsonify(data)
