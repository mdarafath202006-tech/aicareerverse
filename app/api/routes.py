"""
app/api/routes.py — Upgraded REST API
JWT-protected JSON endpoints consumed by the React frontend.
"""
from flask import Blueprint, jsonify, request, session
from app.utils.decorators import login_required, role_required
from app.repositories.alumni_repo import AlumniRepository
from app.repositories.student_repo import StudentRepository
from app.ai.recommender import get_recommendations, get_skill_gap, get_career_analytics
from app.models import Alumni, User

api_bp = Blueprint("api", __name__)


# ── Auth ───────────────────────────────────────────────────────────────────────
@api_bp.route("/auth/login", methods=["POST"])
def api_login():
    data = request.get_json(silent=True) or {}
    email    = str(data.get("email", "")).lower().strip()
    password = str(data.get("password", ""))
    if not email or not password:
        return jsonify({"error": "email and password required"}), 400
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password) or not user.is_active:
        return jsonify({"error": "Invalid credentials"}), 401
    import datetime
    user.last_login = datetime.datetime.utcnow()
    from app.models.base import db
    db.session.commit()
    session.clear()
    session["user_id"] = user.id
    session["name"]    = user.name
    session["role"]    = user.role
    session.permanent  = True
    # JWT token
    try:
        import jwt, os
        payload = {
            "sub": user.id,
            "name": user.name,
            "role": user.role,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        }
        token = jwt.encode(payload, os.getenv("JWT_SECRET_KEY", "jwt-secret"), algorithm="HS256")
    except Exception:
        token = None
    return jsonify({
        "access_token": token,
        "user": user.to_dict(),
    })


# ── Recommendations ────────────────────────────────────────────────────────────
@api_bp.route("/recommendations")
@login_required
def api_recommendations():
    student    = StudentRepository.get_by_user_id(session["user_id"])
    all_alumni = AlumniRepository.get_all_with_users()
    if not student:
        return jsonify({"recommendations": []})
    ranked = get_recommendations(student.to_dict(), all_alumni)
    results = []
    for r in ranked:
        a = r["alumni"]
        results.append({
            "alumni_id":      a.get("id"),
            "name":           a.get("name", ""),
            "job_role":       a.get("job_role", ""),
            "company":        a.get("company", ""),
            "skills":         a.get("skills", ""),
            "location":       a.get("location", ""),
            "linkedin":       a.get("linkedin", ""),
            "bio":            a.get("bio", ""),
            "is_hiring":      a.get("is_hiring", False),
            "score":          r["score"],
            "percent":        r["percent"],
            "skill_overlap":  r["skill_overlap"],
            "matched_skills": r["matched_skills"],
        })
    return jsonify({"recommendations": results})


# ── Analytics ──────────────────────────────────────────────────────────────────
@api_bp.route("/analytics")
@login_required
def api_analytics():
    alumni_data = [
        {"job_role": a.job_role, "company": a.company,
         "skills": a.skills, "graduation_year": a.graduation_year}
        for a in Alumni.query.all()
    ]
    return jsonify(get_career_analytics(alumni_data))


# ── Skill Gap ──────────────────────────────────────────────────────────────────
@api_bp.route("/skill-gap", methods=["POST"])
@login_required
def api_skill_gap():
    data        = request.get_json(silent=True) or {}
    target_role = str(data.get("target_role", "")).strip()
    if not target_role:
        return jsonify({"error": "target_role is required"}), 400
    student    = StudentRepository.get_by_user_id(session["user_id"])
    all_alumni = AlumniRepository.get_all_with_users()
    if not student:
        return jsonify({"error": "Student profile not found"}), 404
    return jsonify(get_skill_gap(student.to_dict(), target_role, all_alumni))


# ── Alumni search ──────────────────────────────────────────────────────────────
@api_bp.route("/alumni")
@login_required
def api_alumni():
    q       = request.args.get("q", "")[:100]
    skill   = request.args.get("skill", "")[:100]
    company = request.args.get("company", "")[:100]
    results = AlumniRepository.search(query=q, skill=skill, company=company)
    return jsonify({"alumni": results})


# ── Alumni profile ─────────────────────────────────────────────────────────────
@api_bp.route("/alumni/<int:alumni_id>")
@login_required
def api_alumni_profile(alumni_id):
    alum = AlumniRepository.get_by_id_with_user(alumni_id)
    if not alum:
        return jsonify({"error": "Not found"}), 404
    return jsonify(alum)


# ── Notifications ──────────────────────────────────────────────────────────────
@api_bp.route("/notifications")
def api_notifications():
    if not session.get("user_id"):
        return jsonify([])
    from app.models import Notification
    notifs = (Notification.query
              .filter_by(user_id=session["user_id"])
              .order_by(Notification.created_at.desc())
              .limit(20).all())
    return jsonify([n.to_dict() for n in notifs])


@api_bp.route("/notifications/<int:nid>/read", methods=["POST"])
def api_mark_read(nid):
    if not session.get("user_id"):
        return jsonify({"error": "Unauthorized"}), 401
    from app.models import Notification
    from app.models.base import db
    n = Notification.query.filter_by(id=nid, user_id=session["user_id"]).first()
    if n:
        n.is_read = True
        db.session.commit()
    return jsonify({"ok": True})


# ── Search ────────────────────────────────────────────────────────────────────
@api_bp.route("/search")
@login_required
def global_search():
    """Global search across users, jobs, companies, posts, communities."""
    q = request.args.get("q", "").strip()[:100]
    if not q or len(q) < 2:
        return jsonify({"results": [], "query": q})

    from app.models import Job, Post, Community, Company
    from app.models.base import db as _db

    results = []

    # Users
    users = (User.query.filter(
        User.name.ilike(f"%{q}%") | User.email.ilike(f"%{q}%")
    ).filter_by(is_active=True).limit(5).all())
    for u in users:
        results.append({"type": "user", "id": u.id, "title": u.name,
                        "subtitle": u.role.title(),
                        "url": f"/alumni/view/{u.alumni.id}" if u.alumni else f"/student/view/{u.student.id}" if u.student else "#"})

    # Jobs
    jobs = Job.query.filter(
        Job.title.ilike(f"%{q}%") | Job.company.ilike(f"%{q}%") | Job.skills_required.ilike(f"%{q}%")
    ).filter_by(is_active=True).limit(5).all()
    for j in jobs:
        results.append({"type": "job", "id": j.id, "title": j.title,
                        "subtitle": f"{j.company} · {j.location or 'India'}",
                        "url": "/jobs"})

    # Companies
    companies = Company.query.filter(
        Company.name.ilike(f"%{q}%") | Company.industry.ilike(f"%{q}%")
    ).limit(3).all()
    for c in companies:
        results.append({"type": "company", "id": c.id, "title": c.name,
                        "subtitle": c.industry or "Technology",
                        "url": f"/companies/{c.slug}"})

    # Communities
    communities = Community.query.filter(
        Community.name.ilike(f"%{q}%") | Community.description.ilike(f"%{q}%")
    ).limit(3).all()
    for c in communities:
        results.append({"type": "community", "id": c.id, "title": c.name,
                        "subtitle": "Community",
                        "url": f"/communities"})

    return jsonify({"results": results, "query": q, "count": len(results)})


# ── Feed Stats ─────────────────────────────────────────────────────────────────
@api_bp.route("/feed/stats")
@login_required
def feed_stats():
    from app.models import Post, Like
    from app.models.base import db as _db
    total_posts = Post.query.count()
    my_likes    = Like.query.filter_by(user_id=session["user_id"]).count()
    return jsonify({"total_posts": total_posts, "my_likes": my_likes})


# ── Profile Completion ─────────────────────────────────────────────────────────
@api_bp.route("/profile/completion")
@login_required
def profile_completion():
    user = User.query.get(session["user_id"])
    if not user:
        return jsonify({"score": 0})
    return jsonify({"score": user.profile_completion(), "name": user.name})
