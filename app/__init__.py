"""
AI CareerVerse V5 — Application Factory
Upgraded: new blueprints, models, SocketIO, CSRF, rate limiting, referrals, companies, knowledge base
"""
import os
from flask import Flask, render_template, session, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit, join_room
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_migrate import Migrate
from app.models.base import db

socketio = SocketIO()
csrf     = CSRFProtect()
limiter  = Limiter(key_func=get_remote_address)
migrate  = Migrate()
_online_users = {}


def create_app(config_object="config.ProductionConfig"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    socketio.init_app(app, cors_allowed_origins="*", async_mode="eventlet")
    csrf.init_app(app)
    limiter.init_app(app)

    with app.app_context():
        from app.models import (  # noqa
            User, Student, Alumni, MentorshipRequest,
            Post, Comment, Like, Notification,
            Community, CommunityMember,
            Job, JobApplication,
            ProjectShowcase, UserPoints, UserBadge,
            Referral, Company, KnowledgeEntry, Follow,
        )

    app.jinja_env.globals.update(
        enumerate=enumerate, zip=zip, len=len, min=min, max=max, int=int
    )

    # ── Blueprints ──────────────────────────────────────
    from app.auth.routes        import auth_bp
    from app.routes.student     import student_bp
    from app.routes.alumni      import alumni_bp
    from app.routes.admin       import admin_bp
    from app.routes.analytics   import analytics_bp
    from app.routes.feed        import feed_bp
    from app.routes.jobs        import jobs_bp
    from app.routes.communities import communities_bp
    from app.routes.referrals   import referrals_bp
    from app.routes.companies   import companies_bp
    from app.routes.knowledge   import knowledge_bp
    from app.routes.ai_routes   import ai_bp
    from app.api.routes         import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp,      url_prefix="/student")
    app.register_blueprint(alumni_bp,       url_prefix="/alumni")
    app.register_blueprint(admin_bp,        url_prefix="/admin")
    app.register_blueprint(analytics_bp)
    app.register_blueprint(feed_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(communities_bp)
    app.register_blueprint(referrals_bp,    url_prefix="/referrals")
    app.register_blueprint(companies_bp,    url_prefix="/companies")
    app.register_blueprint(knowledge_bp,    url_prefix="/knowledge")
    app.register_blueprint(ai_bp,           url_prefix="/ai")
    app.register_blueprint(api_bp,          url_prefix="/api")

    # ── Landing ─────────────────────────────────────────
    @app.route("/")
    def index():
        if session.get("user_id"):
            role = session.get("role")
            if role == "student":   return redirect(url_for("student.dashboard"))
            if role == "alumni":    return redirect(url_for("alumni.dashboard"))
            if role == "admin":     return redirect(url_for("admin.dashboard"))
            if role == "recruiter": return redirect(url_for("jobs.list_jobs"))
            if role == "mentor":    return redirect(url_for("alumni.dashboard"))
        return render_template("index.html")

    # ── AI Tools hub ────────────────────────────────────
    @app.route("/ai-tools")
    def ai_tools():
        if not session.get("user_id"):
            return redirect(url_for("index"))
        return render_template("ai_tools.html")

    # ── Projects ────────────────────────────────────────
    @app.route("/projects")
    def projects():
        if not session.get("user_id"):
            return redirect(url_for("index"))
        from app.models import ProjectShowcase, User
        showcases = (
            db.session.query(ProjectShowcase, User)
            .join(User, ProjectShowcase.user_id == User.id)
            .order_by(ProjectShowcase.created_at.desc())
            .limit(50).all()
        )
        return render_template("projects.html", showcases=showcases)

    # ── Notifications ────────────────────────────────────
    @app.route("/api/notifications")
    def get_notifications():
        if not session.get("user_id"):
            return jsonify([])
        from app.models import Notification
        notifs = (Notification.query
                  .filter_by(user_id=session["user_id"])
                  .order_by(Notification.created_at.desc())
                  .limit(20).all())
        return jsonify([n.to_dict() for n in notifs])

    @app.route("/api/notifications/<int:nid>/read", methods=["POST"])
    def mark_notification_read(nid):
        if not session.get("user_id"):
            return jsonify({"error": "Unauthorized"}), 401
        from app.models import Notification
        n = Notification.query.filter_by(id=nid, user_id=session["user_id"]).first()
        if n:
            n.is_read = True
            db.session.commit()
        return jsonify({"ok": True})

    @app.route("/api/notifications/mark-all-read", methods=["POST"])
    def mark_all_notifications_read():
        if not session.get("user_id"):
            return jsonify({"error": "Unauthorized"}), 401
        from app.models import Notification
        Notification.query.filter_by(user_id=session["user_id"], is_read=False).update({"is_read": True})
        db.session.commit()
        return jsonify({"ok": True})

    # ── SocketIO ─────────────────────────────────────────
    @socketio.on("connect")
    def handle_connect():
        uid = session.get("user_id")
        if uid:
            _online_users[uid] = session.get("name", "User")
            emit("online_count", {"count": len(_online_users)}, broadcast=True)

    @socketio.on("disconnect")
    def handle_disconnect():
        uid = session.get("user_id")
        if uid and uid in _online_users:
            del _online_users[uid]
            emit("online_count", {"count": len(_online_users)}, broadcast=True)

    @socketio.on("join_room")
    def handle_join(data):
        room = str(data.get("room", ""))
        if room:
            join_room(room)
            emit("system_message",
                 {"text": f"{session.get('name','Someone')} joined.", "type": "join"},
                 to=room)

    @socketio.on("send_message")
    def handle_message(data):
        room    = str(data.get("room", ""))
        message = str(data.get("message", "")).strip()[:500]
        if room and message:
            import datetime
            emit("receive_message", {
                "sender":    session.get("name", "Unknown"),
                "role":      session.get("role", ""),
                "message":   message,
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }, to=room)

    @socketio.on("typing")
    def handle_typing(data):
        room = str(data.get("room", ""))
        if room:
            emit("user_typing", {"user": session.get("name", "Someone")},
                 to=room, include_self=False)

    @socketio.on("notification_subscribe")
    def handle_notification_sub():
        uid = session.get("user_id")
        if uid:
            join_room(f"user_{uid}")

    # ── Error handlers ───────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500

    return app
