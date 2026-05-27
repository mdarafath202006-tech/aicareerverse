"""
app/routes/alumni.py — Upgraded Alumni Blueprint (SQLAlchemy ORM)
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required, role_required
from app.repositories.alumni_repo import AlumniRepository
from app.models import db

alumni_bp = Blueprint("alumni", __name__)


@alumni_bp.route("/dashboard")
@login_required
@role_required("alumni")
def dashboard():
    profile = AlumniRepository.get_by_user_id(session["user_id"])
    requests_raw = []
    accepted_count = 0
    if profile:
        rows = AlumniRepository.get_pending_requests(profile.id)
        for req, student, user in rows:
            r = req.to_dict()
            r["student_name"] = user.name
            r["department"]   = student.department
            r["year"]         = student.year
            r["skills"]       = student.skills
            requests_raw.append(r)
        from app.models import MentorshipRequest
        accepted_count = MentorshipRequest.query.filter_by(alumni_id=profile.id, status="accepted").count()
    return render_template("alumni/dashboard.html",
                           profile=profile.to_dict() if profile else {},
                           requests=requests_raw, accepted_count=accepted_count)


@alumni_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("alumni")
def profile():
    alum = AlumniRepository.get_by_user_id(session["user_id"])
    if request.method == "POST":
        try:
            from app.schemas.user_schemas import AlumniProfileSchema
            data = AlumniProfileSchema().load(request.form)
            for k, v in data.items():
                if hasattr(alum, k):
                    setattr(alum, k, v)
            db.session.commit()
            flash("Profile updated!", "success")
        except Exception as e:
            flash(str(e), "danger")
    return render_template("alumni/profile.html", profile=alum.to_dict() if alum else {})


@alumni_bp.route("/respond/<int:req_id>/<action>")
@login_required
@role_required("alumni")
def respond_request(req_id, action):
    if action not in ("accept", "reject"):
        flash("Invalid action.", "danger")
        return redirect(url_for("alumni.dashboard"))
    status = "accepted" if action == "accept" else "rejected"
    req    = AlumniRepository.update_request_status(req_id, status)
    if req and status == "accepted":
        try:
            from app.models import Student, User
            student     = Student.query.get(req.student_id)
            student_user = User.query.get(student.user_id) if student else None
            alum_profile = AlumniRepository.get_by_user_id(session["user_id"])
            alum_user    = User.query.get(alum_profile.user_id) if alum_profile else None
            if student_user and alum_user:
                from app.tasks.notification_tasks import send_mentor_accepted
                send_mentor_accepted.delay(student_user.id, alum_user.name, req_id)
        except Exception:
            pass
    flash(f"Request {status}.", "success")
    return redirect(url_for("alumni.dashboard"))


@alumni_bp.route("/view/<int:alumni_id>")
@login_required
def view(alumni_id):
    alum = AlumniRepository.get_by_id_with_user(alumni_id)
    if not alum:
        flash("Alumni not found.", "danger")
        return redirect(url_for("student.search"))
    return render_template("view_alumni.html", alumni=alum)
