"""app/routes/referrals.py — Referral System V5"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from app.utils.decorators import login_required, role_required
from app.models import db, Referral, Student, Alumni, User, Notification, Job
from app import socketio

referrals_bp = Blueprint("referrals", __name__)


@referrals_bp.route("/")
@login_required
def index():
    """Show referrals for current user."""
    role = session.get("role")
    if role == "student":
        student = Student.query.filter_by(user_id=session["user_id"]).first()
        if not student:
            flash("Student profile not found.", "danger")
            return redirect(url_for("student.dashboard"))
        rows = (
            db.session.query(Referral, Alumni, User)
            .join(Alumni, Referral.alumni_id == Alumni.id)
            .join(User, Alumni.user_id == User.id)
            .filter(Referral.student_id == student.id)
            .order_by(Referral.created_at.desc())
            .all()
        )
        referrals = []
        for ref, alum, alum_user in rows:
            d = ref.to_dict()
            d["alumni_name"]    = alum_user.name
            d["alumni_company"] = alum.company
            d["alumni_role"]    = alum.job_role
            d["alumni_avatar"]  = alum_user.avatar_url
            referrals.append(d)
        return render_template("referrals/student_referrals.html", referrals=referrals)

    elif role == "alumni":
        alum = Alumni.query.filter_by(user_id=session["user_id"]).first()
        if not alum:
            return redirect(url_for("alumni.dashboard"))
        rows = (
            db.session.query(Referral, Student, User)
            .join(Student, Referral.student_id == Student.id)
            .join(User, Student.user_id == User.id)
            .filter(Referral.alumni_id == alum.id)
            .order_by(Referral.created_at.desc())
            .all()
        )
        referrals = []
        for ref, stu, stu_user in rows:
            d = ref.to_dict()
            d["student_name"]   = stu_user.name
            d["student_dept"]   = stu.department
            d["student_year"]   = stu.year
            d["student_skills"] = stu.skills
            d["student_avatar"] = stu_user.avatar_url
            referrals.append(d)
        return render_template("referrals/alumni_referrals.html", referrals=referrals)

    return redirect(url_for("index"))


@referrals_bp.route("/request/<int:alumni_id>", methods=["GET", "POST"])
@login_required
@role_required("student")
def request_referral(alumni_id):
    """Student requests referral from an alumni."""
    student = Student.query.filter_by(user_id=session["user_id"]).first()
    alum = Alumni.query.get_or_404(alumni_id)
    alum_user = User.query.get(alum.user_id)

    if request.method == "POST":
        company  = request.form.get("company", "")[:150]
        position = request.form.get("position", "")[:150]
        message  = request.form.get("message", "")[:1000]

        # Check if already requested
        existing = Referral.query.filter_by(
            student_id=student.id, alumni_id=alumni_id
        ).first()
        if existing:
            flash("You already have a referral request with this alumni.", "warning")
            return redirect(url_for("referrals.index"))

        ref = Referral(
            student_id=student.id, alumni_id=alumni_id,
            company=company, position=position, message=message,
        )
        db.session.add(ref)

        # Notify alumni
        n = Notification(
            user_id=alum.user_id, type="referral_request",
            title="New Referral Request",
            message=f"{session.get('name','A student')} requested a referral for {position} at {company}.",
            link="/referrals/"
        )
        db.session.add(n)
        db.session.commit()

        try:
            socketio.emit("live_notification", n.to_dict(), to=f"user_{alum.user_id}")
        except Exception:
            pass

        flash("Referral request sent! 🎉", "success")
        return redirect(url_for("referrals.index"))

    jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(20).all()
    return render_template("referrals/request_referral.html",
                           alum=alum, alum_user=alum_user, jobs=jobs)


@referrals_bp.route("/respond/<int:ref_id>/<action>", methods=["POST"])
@login_required
@role_required("alumni")
def respond_referral(ref_id, action):
    """Alumni approves or rejects referral."""
    if action not in ("approve", "reject"):
        return jsonify({"error": "Invalid action"}), 400

    alum = Alumni.query.filter_by(user_id=session["user_id"]).first()
    ref  = Referral.query.filter_by(id=ref_id, alumni_id=alum.id).first_or_404()

    ref.status      = "approved" if action == "approve" else "rejected"
    ref.alumni_note = request.form.get("note", "")[:500]
    db.session.commit()

    # Notify student
    student     = Student.query.get(ref.student_id)
    stu_user    = User.query.get(student.user_id) if student else None
    alum_user   = User.query.get(session["user_id"])
    if stu_user:
        icon  = "✅" if ref.status == "approved" else "❌"
        n = Notification(
            user_id=stu_user.id, type=f"referral_{ref.status}",
            title=f"Referral {ref.status.title()}! {icon}",
            message=f"{alum_user.name if alum_user else 'Alumni'} {ref.status} your referral request for {ref.position}.",
            link="/referrals/"
        )
        db.session.add(n)
        db.session.commit()
        try:
            socketio.emit("live_notification", n.to_dict(), to=f"user_{stu_user.id}")
        except Exception:
            pass

    flash(f"Referral {ref.status}.", "success")
    return redirect(url_for("referrals.index"))
