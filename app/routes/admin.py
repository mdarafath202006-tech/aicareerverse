"""app/routes/admin.py — Admin Dashboard V5"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.utils.decorators import login_required, role_required
from app.models import db, User, Student, Alumni, MentorshipRequest, Post, Job, JobApplication, Referral, KnowledgeEntry

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    stats = {
        "total_users":       User.query.count(),
        "students":          Student.query.count(),
        "alumni":            Alumni.query.count(),
        "mentorships":       MentorshipRequest.query.filter_by(status="accepted").count(),
        "pending_mentors":   MentorshipRequest.query.filter_by(status="pending").count(),
        "posts":             Post.query.count(),
        "jobs":              Job.query.filter_by(is_active=True).count(),
        "applications":      JobApplication.query.count(),
        "referrals":         Referral.query.count(),
        "knowledge_entries": KnowledgeEntry.query.count(),
        "hiring_alumni":     Alumni.query.filter_by(is_hiring=True).count(),
    }
    recent_users      = User.query.order_by(User.created_at.desc()).limit(20).all()
    recent_posts      = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    recent_jobs       = Job.query.order_by(Job.created_at.desc()).limit(10).all()
    pending_referrals = Referral.query.filter_by(status="pending").order_by(Referral.created_at.desc()).limit(10).all()
    return render_template(
        "admin/dashboard.html",
        stats=stats, recent_users=recent_users,
        recent_posts=recent_posts, recent_jobs=recent_jobs,
        pending_referrals=pending_referrals,
    )


@admin_bp.route("/users")
@login_required
@role_required("admin")
def users():
    role_filter = request.args.get("role", "")
    q           = request.args.get("q", "")
    query       = User.query
    if role_filter:
        query = query.filter_by(role=role_filter)
    if q:
        query = query.filter(User.name.ilike(f"%{q}%") | User.email.ilike(f"%{q}%"))
    all_users = query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users, role_filter=role_filter, q=q)


@admin_bp.route("/users/<int:uid>/toggle", methods=["POST"])
@login_required
@role_required("admin")
def toggle_user(uid):
    user = User.query.get_or_404(uid)
    user.is_active = not user.is_active
    db.session.commit()
    flash(f"User {'activated' if user.is_active else 'deactivated'}.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/analytics")
@login_required
@role_required("admin")
def analytics():
    from app.models import Community, CommunityMember
    stats = {
        "total_users": User.query.count(),
        "students":    Student.query.count(),
        "alumni":      Alumni.query.count(),
        "jobs":        Job.query.count(),
        "posts":       Post.query.count(),
        "mentorships_total":   MentorshipRequest.query.count(),
        "mentorships_accepted": MentorshipRequest.query.filter_by(status="accepted").count(),
        "referrals_total":     Referral.query.count(),
        "referrals_approved":  Referral.query.filter_by(status="approved").count(),
        "applications":        JobApplication.query.count(),
    }
    return render_template("admin/analytics.html", stats=stats)
