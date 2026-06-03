"""
app/routes/alumni.py — Alumni Blueprint V3
Handles dashboard, profile management, mentorship response.
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
    profile        = AlumniRepository.get_by_user_id(session["user_id"])
    requests_raw   = []
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
        accepted_count = (MentorshipRequest.query
                          .filter_by(alumni_id=profile.id, status="accepted")
                          .count())
    return render_template(
        "alumni/dashboard.html",
        profile=profile.to_dict() if profile else {},
        requests=requests_raw,
        accepted_count=accepted_count,
    )


@alumni_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("alumni")
def profile():
    alum = AlumniRepository.get_by_user_id(session["user_id"])
    if request.method == "POST":
        try:
            fields = ["company", "job_role", "location", "skills", "bio",
                      "domain", "linkedin", "graduation_year", "mentorship_slots"]
            for f in fields:
                val = request.form.get(f)
                if val is not None and hasattr(alum, f):
                    # Cast numeric fields
                    if f in ("graduation_year", "mentorship_slots"):
                        try:
                            setattr(alum, f, int(val))
                        except (ValueError, TypeError):
                            pass
                    else:
                        setattr(alum, f, str(val)[:500])
            alum.is_hiring = bool(request.form.get("is_hiring"))
            db.session.commit()
            flash("Profile updated successfully! ✅", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Update failed: {e}", "danger")
        return redirect(url_for("alumni.profile"))
    return render_template("alumni/profile.html",
                           profile=alum.to_dict() if alum else {})


@alumni_bp.route("/mentorship")
@login_required
@role_required("alumni")
def mentorship():
    profile = AlumniRepository.get_by_user_id(session["user_id"])
    if not profile:
        return redirect(url_for("alumni.dashboard"))
    rows = AlumniRepository.get_pending_requests(profile.id)
    requests_raw = []
    for req, student, user in rows:
        r = req.to_dict()
        r["student_name"] = user.name
        r["department"]   = student.department
        r["year"]         = student.year
        r["skills"]       = student.skills
        requests_raw.append(r)
    return render_template("alumni/mentorship.html", requests=requests_raw)


@alumni_bp.route("/respond/<int:req_id>/<action>")
@login_required
@role_required("alumni")
def respond_request(req_id, action):
    if action not in ("accept", "reject"):
        flash("Invalid action.", "danger")
        return redirect(url_for("alumni.dashboard"))
    status = "accepted" if action == "accept" else "rejected"
    req    = AlumniRepository.update_request_status(req_id, status)
    if req:
        # Notify student
        try:
            from app.models import Student, User, Notification
            student      = Student.query.get(req.student_id)
            student_user = User.query.get(student.user_id) if student else None
            alum_profile = AlumniRepository.get_by_user_id(session["user_id"])
            from app.models import User as U
            alum_user    = U.query.get(session["user_id"])
            if student_user:
                icon    = "✅" if status == "accepted" else "❌"
                title   = f"Mentorship {status.title()}! {icon}"
                message = (f"{alum_user.name if alum_user else 'Alumni'} "
                           f"{'accepted' if status=='accepted' else 'declined'} "
                           f"your mentorship request.")
                n = Notification(
                    user_id=student_user.id, type=f"mentor_{status}",
                    title=title, message=message,
                    link="/student/mentorship",
                )
                db.session.add(n)
                db.session.commit()
                from app import socketio
                socketio.emit("live_notification", n.to_dict(),
                              to=f"user_{student_user.id}")
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


@alumni_bp.route("/search")
@login_required
def alumni_search():
    """Public-facing alumni browse for any logged-in user."""
    from app.models import Alumni, User
    q      = request.args.get("q", "").strip()
    domain = request.args.get("domain", "").strip()

    query = (db.session.query(Alumni, User)
             .join(User, Alumni.user_id == User.id)
             .filter(User.is_active == True))
    if q:
        query = query.filter(
            User.name.ilike(f"%{q}%") |
            Alumni.company.ilike(f"%{q}%") |
            Alumni.skills.ilike(f"%{q}%") |
            Alumni.domain.ilike(f"%{q}%")
        )
    if domain:
        query = query.filter(Alumni.domain.ilike(f"%{domain}%"))

    rows = query.order_by(Alumni.impact_score.desc()).limit(40).all()
    results = []
    for alum, user in rows:
        d = alum.to_dict()
        d["name"]       = user.name
        d["avatar_url"] = user.avatar_url
        results.append(d)
    domains = [r[0] for r in db.session.query(Alumni.domain).distinct().filter(Alumni.domain != None).order_by(Alumni.domain).all()]
    return render_template("alumni/search.html", results=results, domains=domains, q=q, domain=domain)


@alumni_bp.route("/view/<int:alumni_id>")
@login_required
def view_alumni(alumni_id):
    """Public alumni profile page with referral + mentorship CTA."""
    from app.models import Alumni, User, MentorshipRequest, Referral, Student, Follow
    alum = Alumni.query.get_or_404(alumni_id)
    user = User.query.get_or_404(alum.user_id)

    # Check if current student already has requests
    has_mentor_request = False
    has_referral       = False
    is_following       = False
    if session.get("role") == "student":
        student = db.session.query(Alumni).filter_by(user_id=session["user_id"]).first()
        from app.repositories.student_repo import StudentRepository
        stu = StudentRepository.get_by_user_id(session["user_id"])
        if stu:
            has_mentor_request = MentorshipRequest.query.filter_by(
                student_id=stu.id, alumni_id=alumni_id
            ).first() is not None
            has_referral = Referral.query.filter_by(
                student_id=stu.id, alumni_id=alumni_id
            ).first() is not None
        is_following = Follow.query.filter_by(
            follower_id=session["user_id"], following_id=alum.user_id
        ).first() is not None

    # Recent knowledge entries by this alumni
    from app.models import KnowledgeEntry
    stories = KnowledgeEntry.query.filter_by(
        author_id=user.id, is_approved=True
    ).order_by(KnowledgeEntry.created_at.desc()).limit(3).all()

    return render_template("alumni/view_profile.html",
                           alum=alum, user=user, stories=stories,
                           has_mentor_request=has_mentor_request,
                           has_referral=has_referral,
                           is_following=is_following)
