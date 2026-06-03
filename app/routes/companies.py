"""app/routes/companies.py — Company Pages V5"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.utils.decorators import login_required, role_required
from app.models import db, Company, Job, Alumni, User

companies_bp = Blueprint("companies", __name__)


@companies_bp.route("/")
@login_required
def index():
    companies = Company.query.order_by(Company.name).all()
    for c in companies:
        c._job_count = Job.query.filter_by(company=c.name, is_active=True).count()
        c._alumni_count = Alumni.query.filter(Alumni.company.ilike(f"%{c.name}%")).count()
    return render_template("companies/index.html", companies=companies)


@companies_bp.route("/<slug>")
@login_required
def detail(slug):
    company = Company.query.filter_by(slug=slug).first_or_404()
    jobs    = Job.query.filter_by(company=company.name, is_active=True).order_by(Job.created_at.desc()).all()
    alumni_rows = (
        db.session.query(Alumni, User)
        .join(User, Alumni.user_id == User.id)
        .filter(Alumni.company.ilike(f"%{company.name}%"))
        .limit(10).all()
    )
    alumni = [{"profile": a.to_dict(), "user": u.to_dict()} for a, u in alumni_rows]
    return render_template("companies/detail.html", company=company, jobs=jobs, alumni=alumni)
