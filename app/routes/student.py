"""
app/routes/student.py — Upgraded Student Blueprint
Uses: SQLAlchemy ORM via repositories, Celery tasks, Marshmallow validation
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.utils.decorators import login_required, role_required
from app.repositories.student_repo import StudentRepository
from app.repositories.alumni_repo import AlumniRepository
from app.ai.recommender import get_recommendations, get_skill_gap
from marshmallow import ValidationError

student_bp = Blueprint("student", __name__)


@student_bp.route("/dashboard")
@login_required
@role_required("student")
def dashboard():
    student = StudentRepository.get_by_user_id(session["user_id"])
    stats   = StudentRepository.get_stats(student.id) if student else {}
    return render_template("student/dashboard.html", profile=student.to_dict() if student else {}, **stats)


@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("student")
def profile():
    student = StudentRepository.get_by_user_id(session["user_id"])
    if request.method == "POST":
        try:
            from app.schemas.user_schemas import StudentProfileSchema
            data = StudentProfileSchema().load(request.form)
            StudentRepository.update_profile(student, **data)
            flash("Profile updated!", "success")
            # Trigger async AI score recomputation
            try:
                from app.tasks.ai_tasks import recompute_recommendations
                recompute_recommendations.delay(student.id)
            except Exception:
                pass
        except ValidationError as e:
            flash(str(e.messages), "danger")
    return render_template("student/profile.html", profile=student.to_dict() if student else {})


@student_bp.route("/recommendations")
@login_required
@role_required("student")
def recommendations():
    student    = StudentRepository.get_by_user_id(session["user_id"])
    all_alumni = AlumniRepository.get_all_with_users()
    ranked     = []
    if student and (student.skills or student.interests):
        ranked = get_recommendations(student.to_dict(), all_alumni)
    else:
        ranked = [{"alumni": a, "score": 0, "percent": 0, "matched_skills": [], "skill_overlap": 0}
                  for a in all_alumni]
    return render_template("student/recommendations.html", ranked=ranked,
                           student=student.to_dict() if student else {})


@student_bp.route("/skill-gap")
@login_required
@role_required("student")
def skill_gap():
    student     = StudentRepository.get_by_user_id(session["user_id"])
    all_alumni  = AlumniRepository.get_all_with_users()
    roles       = AlumniRepository.distinct_roles()
    target_role = request.args.get("role", "")
    gap_data    = {}
    if target_role and student:
        gap_data = get_skill_gap(student.to_dict(), target_role, all_alumni)
    return render_template("student/skill_gap.html",
                           student=student.to_dict() if student else {},
                           roles=roles, target_role=target_role, gap=gap_data)


@student_bp.route("/request_mentor/<int:alumni_id>", methods=["POST"])
@login_required
@role_required("student")
def request_mentor(alumni_id):
    student = StudentRepository.get_by_user_id(session["user_id"])
    if not student:
        flash("Student profile not found.", "danger")
        return redirect(url_for("student.recommendations"))
    message = request.form.get("message", "")[:500]
    if StudentRepository.has_pending_request(student.id, alumni_id):
        flash("You already have a pending request to this mentor.", "warning")
        return redirect(url_for("student.recommendations"))
    req = StudentRepository.send_request(student.id, alumni_id, message)
    # Notify alumni async
    try:
        alum = AlumniRepository.get_by_id_with_user(alumni_id)
        if alum:
            from app.tasks.notification_tasks import send_mentor_request_alert
            from app.models import User
            alum_user = User.query.get(alum["user_id"])
            send_mentor_request_alert.delay(alum_user.id, session.get("name", "A student"))
    except Exception:
        pass
    flash("Mentorship request sent!", "success")
    return redirect(url_for("student.recommendations"))


@student_bp.route("/search")
@login_required
@role_required("student")
def search():
    query   = request.args.get("q", "")[:100]
    skill   = request.args.get("skill", "")[:100]
    company = request.args.get("company", "")[:100]
    results = AlumniRepository.search(query=query, skill=skill, company=company)
    return render_template("student/search.html",
                           results=results, query=query, skill=skill, company=company)
