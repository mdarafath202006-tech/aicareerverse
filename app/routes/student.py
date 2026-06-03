"""
app/routes/student.py — Student Blueprint V3
Handles dashboard, profile, mentorship requests, recommendations, skill gap, search.
"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required, role_required
from app.repositories.student_repo import StudentRepository
from app.repositories.alumni_repo import AlumniRepository
from app.ai.recommender import get_recommendations, get_skill_gap

student_bp = Blueprint("student", __name__)


@student_bp.route("/dashboard")
@login_required
@role_required("student")
def dashboard():
    student = StudentRepository.get_by_user_id(session["user_id"])
    stats   = StudentRepository.get_stats(student.id) if student else {}
    return render_template(
        "student/dashboard.html",
        profile=student.to_dict() if student else {},
        **stats,
    )


@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("student")
def profile():
    student = StudentRepository.get_by_user_id(session["user_id"])
    if request.method == "POST":
        try:
            fields = ["department", "year", "skills", "interests", "bio",
                      "github_url", "linkedin_url", "resume_url"]
            data = {f: (request.form.get(f) or "")[:500] for f in fields}
            StudentRepository.update_profile(student, **data)
            # Async AI recompute — graceful if celery not available
            try:
                from app.tasks.ai_tasks import recompute_recommendations
                recompute_recommendations.delay(student.id)
            except Exception:
                pass
            flash("Profile updated successfully! ✅", "success")
        except Exception as e:
            flash(f"Update failed: {e}", "danger")
        return redirect(url_for("student.profile"))
    return render_template("student/profile.html",
                           profile=student.to_dict() if student else {})


@student_bp.route("/recommendations")
@login_required
@role_required("student")
def recommendations():
    student    = StudentRepository.get_by_user_id(session["user_id"])
    all_alumni = AlumniRepository.get_all_with_users()
    if student and (student.skills or student.interests):
        ranked = get_recommendations(student.to_dict(), all_alumni)
    else:
        ranked = [{"alumni": a, "score": 0, "percent": 0,
                   "matched_skills": [], "skill_overlap": 0}
                  for a in all_alumni]
    return render_template("student/recommendations.html",
                           ranked=ranked,
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
        raw = get_skill_gap(student.to_dict(), target_role, all_alumni)
        # Normalise keys for template: 'missing', 'matched'
        gap_data = {
            "missing":  raw.get("missing", []),
            "matched":  raw.get("student_has", []),
            "required": raw.get("required_skills", []),
            "coverage": raw.get("coverage_pct", 0),
        }
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
    message = (request.form.get("message") or "")[:500]
    if StudentRepository.has_pending_request(student.id, alumni_id):
        flash("You already sent a request to this mentor.", "warning")
        return redirect(request.referrer or url_for("student.recommendations"))
    StudentRepository.send_request(student.id, alumni_id, message)
    # Notify alumni (graceful)
    try:
        from app.models import Notification, Alumni, User
        alum_profile = Alumni.query.get(alumni_id)
        if alum_profile:
            n = Notification(
                user_id=alum_profile.user_id,
                type="mentor_request",
                title="New Mentorship Request",
                message=f"{session.get('name','A student')} sent you a mentorship request.",
                link="/alumni/mentorship",
            )
            from app.models.base import db
            db.session.add(n)
            db.session.commit()
            # Real-time push
            from app import socketio
            socketio.emit("live_notification", n.to_dict(),
                          to=f"user_{alum_profile.user_id}")
    except Exception:
        pass
    flash("Mentorship request sent! 🎉", "success")
    return redirect(request.referrer or url_for("student.recommendations"))


@student_bp.route("/mentorship")
@login_required
@role_required("student")
def mentorship():
    from app.models import MentorshipRequest, Alumni, User
    student = StudentRepository.get_by_user_id(session["user_id"])
    if not student:
        return redirect(url_for("student.dashboard"))
    rows = (
        MentorshipRequest.query
        .filter_by(student_id=student.id)
        .order_by(MentorshipRequest.created_at.desc())
        .all()
    )
    from app.models.base import db
    requests_data = []
    for req in rows:
        d = req.to_dict()
        alum_profile = Alumni.query.get(req.alumni_id)
        alum_user    = User.query.get(alum_profile.user_id) if alum_profile else None
        d["alumni_name"]    = alum_user.name    if alum_user    else "Unknown"
        d["alumni_company"] = alum_profile.company  if alum_profile else ""
        d["alumni_role"]    = alum_profile.job_role if alum_profile else ""
        d["alumni_id"]      = req.alumni_id
        requests_data.append(d)
    return render_template("student/mentorship.html", requests=requests_data)


@student_bp.route("/search")
@login_required
@role_required("student")
def search():
    query   = (request.args.get("q")   or "")[:100]
    skill   = (request.args.get("skill")   or "")[:100]
    company = (request.args.get("company") or "")[:100]
    results = AlumniRepository.search(query=query, skill=skill, company=company)
    return render_template("student/search.html",
                           results=results, query=query,
                           skill=skill, company=company)


@student_bp.route("/search")
@login_required
@role_required("student")
def search():
    """Alumni search with filters."""
    q        = request.args.get("q", "").strip()
    company  = request.args.get("company", "").strip()
    domain   = request.args.get("domain", "").strip()
    hiring   = request.args.get("hiring", "").strip()

    from app.models import Alumni, User
    from app.models.base import db

    query = (db.session.query(Alumni, User)
             .join(User, Alumni.user_id == User.id)
             .filter(User.is_active == True))

    if q:
        query = query.filter(
            User.name.ilike(f"%{q}%") |
            Alumni.company.ilike(f"%{q}%") |
            Alumni.skills.ilike(f"%{q}%") |
            Alumni.domain.ilike(f"%{q}%") |
            Alumni.job_role.ilike(f"%{q}%")
        )
    if company:
        query = query.filter(Alumni.company.ilike(f"%{company}%"))
    if domain:
        query = query.filter(Alumni.domain.ilike(f"%{domain}%"))
    if hiring == "1":
        query = query.filter(Alumni.is_hiring == True)

    rows = query.order_by(Alumni.impact_score.desc()).limit(50).all()
    results = []
    for alum, user in rows:
        d = alum.to_dict()
        d["name"]       = user.name
        d["avatar_url"] = user.avatar_url
        results.append(d)

    # Distinct companies / domains for filter dropdowns
    companies = [r[0] for r in db.session.query(Alumni.company).distinct().filter(Alumni.company != None).order_by(Alumni.company).all()]
    domains   = [r[0] for r in db.session.query(Alumni.domain).distinct().filter(Alumni.domain != None).order_by(Alumni.domain).all()]

    return render_template("student/search.html",
                           results=results,
                           companies=companies, domains=domains,
                           q=q, company=company, domain=domain, hiring=hiring)


@student_bp.route("/mentorship")
@login_required
@role_required("student")
def mentorship():
    """Student view of their own mentorship requests."""
    from app.models import MentorshipRequest, Alumni, User
    from app.models.base import db
    student = StudentRepository.get_by_user_id(session["user_id"])
    if not student:
        return redirect(url_for("student.dashboard"))

    rows = (db.session.query(MentorshipRequest, Alumni, User)
            .join(Alumni, MentorshipRequest.alumni_id == Alumni.id)
            .join(User, Alumni.user_id == User.id)
            .filter(MentorshipRequest.student_id == student.id)
            .order_by(MentorshipRequest.created_at.desc())
            .all())
    requests = []
    for req, alum, alum_user in rows:
        d = req.to_dict()
        d["alumni_name"]   = alum_user.name
        d["alumni_company"]= alum.company
        d["alumni_role"]   = alum.job_role
        d["alumni_avatar"] = alum_user.avatar_url
        requests.append(d)

    return render_template("student/mentorship.html", requests=requests)


@student_bp.route("/follow/<int:target_user_id>", methods=["POST"])
@login_required
def follow_user(target_user_id):
    """Follow/unfollow a user."""
    from app.models import Follow
    from app.models.base import db
    uid = session["user_id"]
    if uid == target_user_id:
        return {"error": "Cannot follow yourself"}, 400

    existing = Follow.query.filter_by(follower_id=uid, following_id=target_user_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        return {"status": "unfollowed"}
    else:
        db.session.add(Follow(follower_id=uid, following_id=target_user_id))
        db.session.commit()
        return {"status": "followed"}


@student_bp.route("/view/<int:student_id>")
@login_required
def view_student(student_id):
    """Public student profile view."""
    from app.models import Student, User, ProjectShowcase
    from app.models.base import db
    student = Student.query.get_or_404(student_id)
    user    = User.query.get_or_404(student.user_id)
    projects = ProjectShowcase.query.filter_by(user_id=user.id).limit(6).all()
    return render_template("student/view_profile.html",
                           student=student, user=user, projects=projects)
