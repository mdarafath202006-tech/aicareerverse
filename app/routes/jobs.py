"""app/routes/jobs.py"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required, role_required
from app.models import db, Job, JobApplication, User

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/jobs")
@login_required
def list_jobs():
    q        = request.args.get("q", "")
    job_type = request.args.get("type", "")
    query    = Job.query.filter_by(is_active=True)
    if q:
        query = query.filter(
            Job.title.ilike(f"%{q}%") |
            Job.company.ilike(f"%{q}%") |
            Job.description.ilike(f"%{q}%")
        )
    if job_type:
        query = query.filter_by(job_type=job_type)
    jobs = query.order_by(Job.created_at.desc()).all()
    return render_template("jobs.html", jobs=jobs, q=q, job_type=job_type)


@jobs_bp.route("/jobs/post", methods=["GET", "POST"])
@login_required
@role_required("alumni", "admin")
def post_job():
    if request.method == "POST":
        job = Job(
            posted_by       = session["user_id"],
            title           = request.form.get("title", "")[:200],
            company         = request.form.get("company", "")[:150],
            location        = request.form.get("location", "")[:150],
            job_type        = request.form.get("job_type", "full_time"),
            description     = request.form.get("description", "")[:5000],
            requirements    = request.form.get("requirements", "")[:5000],
            skills_required = request.form.get("skills_required", "")[:500],
            salary_range    = request.form.get("salary_range", "")[:100],
            apply_url       = request.form.get("apply_url", "")[:500],
        )
        db.session.add(job)
        db.session.commit()
        flash("Job posted successfully! 🎉", "success")
        return redirect(url_for("jobs.list_jobs"))
    return render_template("post_job.html")


@jobs_bp.route("/jobs/apply/<int:job_id>", methods=["POST"])
@login_required
def apply_job(job_id):
    existing = JobApplication.query.filter_by(job_id=job_id, user_id=session["user_id"]).first()
    if existing:
        flash("You already applied for this job.", "warning")
        return redirect(url_for("jobs.list_jobs"))
    app = JobApplication(
        job_id=job_id, user_id=session["user_id"],
        cover_letter=request.form.get("cover_letter", "")[:2000],
    )
    db.session.add(app)
    db.session.commit()
    flash("Application submitted! Good luck! 🚀", "success")
    return redirect(url_for("jobs.list_jobs"))
