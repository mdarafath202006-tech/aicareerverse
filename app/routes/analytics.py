"""app/routes/analytics.py — Analytics with real DB stats"""
from flask import Blueprint, render_template, jsonify, session
from app.utils.decorators import login_required
from app.ai.recommender import get_career_analytics
from app.models import db, Alumni, User, Student, MentorshipRequest, Post

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
@login_required
def analytics():
    alumni_data = [
        {"job_role": a.job_role, "company": a.company,
         "skills": a.skills, "graduation_year": a.graduation_year}
        for a in Alumni.query.all()
    ]
    data = get_career_analytics(alumni_data)
    stats = {
        "total_users":  User.query.count(),
        "students":     Student.query.count(),
        "alumni":       Alumni.query.count(),
        "mentorships":  MentorshipRequest.query.filter_by(status="accepted").count(),
        "posts":        Post.query.count(),
    }
    return render_template("analytics.html", data=data, stats=stats)


@analytics_bp.route("/api/analytics/live")
@login_required
def live_analytics():
    alumni_data = [
        {"job_role": a.job_role, "company": a.company,
         "skills": a.skills, "graduation_year": a.graduation_year}
        for a in Alumni.query.all()
    ]
    return jsonify(get_career_analytics(alumni_data))
