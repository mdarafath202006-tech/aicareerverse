"""
AI CareerVerse — Upgraded Application Factory
Phase 1-4 Upgrades: SQLAlchemy ORM, Flask-Migrate, Celery+Redis, Enhanced SocketIO
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
        from app.models import User, Student, Alumni, MentorshipRequest, Post, Notification  # noqa

    app.jinja_env.globals.update(enumerate=enumerate, zip=zip, len=len, min=min, max=max)

    from app.auth.routes      import auth_bp
    from app.routes.student   import student_bp
    from app.routes.alumni    import alumni_bp
    from app.routes.admin     import admin_bp
    from app.routes.analytics import analytics_bp
    from app.api.routes       import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp,  url_prefix="/student")
    app.register_blueprint(alumni_bp,   url_prefix="/alumni")
    app.register_blueprint(admin_bp,    url_prefix="/admin")
    app.register_blueprint(analytics_bp)
    app.register_blueprint(api_bp,      url_prefix="/api")

    @app.route("/")
    def index():
        if session.get("user_id"):
            role = session.get("role")
            if role == "student": return redirect(url_for("student.dashboard"))
            if role == "alumni":  return redirect(url_for("alumni.dashboard"))
            if role == "admin":   return redirect(url_for("admin.dashboard"))
        return render_template("index.html")

    @app.route("/api/notifications")
    def get_notifications():
        if not session.get("user_id"):
            return jsonify([])
        from app.models import Notification
        notifs = (Notification.query.filter_by(user_id=session["user_id"])
                  .order_by(Notification.created_at.desc()).limit(20).all())
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
            emit("system_message", {"text": f"{session.get('name','Someone')} joined.", "type": "join"}, to=room)

    @socketio.on("send_message")
    def handle_message(data):
        room    = str(data.get("room", ""))
        message = str(data.get("message", "")).strip()[:500]
        if room and message:
            import datetime
            emit("receive_message", {
                "sender": session.get("name", "Unknown"), "role": session.get("role", ""),
                "message": message, "timestamp": datetime.datetime.utcnow().isoformat(),
            }, to=room)

    @socketio.on("typing")
    def handle_typing(data):
        room = str(data.get("room", ""))
        if room:
            emit("user_typing", {"user": session.get("name", "Someone")}, to=room, include_self=False)

    @socketio.on("notification_subscribe")
    def handle_notification_sub():
        uid = session.get("user_id")
        if uid:
            join_room(f"user_{uid}")

    @app.errorhandler(404)
    def not_found(e):
        return ("<div style='text-align:center;padding:4rem;font-family:sans-serif;"
                "background:#050508;color:#e8eaf6;min-height:100vh'>"
                "<h1 style='font-size:4rem'>404</h1><p>Page not found</p>"
                "<a href='/' style='color:#6366f1'>← Go Home</a></div>", 404)

    @app.errorhandler(500)
    def server_error(e):
        return ("<div style='text-align:center;padding:4rem;font-family:sans-serif'>"
                "<h1>500 — Server Error</h1><a href='/'>← Go Home</a></div>", 500)

    return app
