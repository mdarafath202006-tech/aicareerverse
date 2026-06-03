"""app/models/gamification.py"""
from datetime import datetime
from .base import db


class UserPoints(db.Model):
    __tablename__ = "user_points"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    total      = db.Column(db.Integer, default=0)
    mentoring  = db.Column(db.Integer, default=0)
    posting    = db.Column(db.Integer, default=0)
    helping    = db.Column(db.Integer, default=0)
    engagement = db.Column(db.Integer, default=0)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id])


class UserBadge(db.Model):
    __tablename__ = "user_badges"

    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    badge_type = db.Column(db.String(50), nullable=False)  # top_mentor, active_contributor, etc.
    badge_name = db.Column(db.String(100))
    badge_icon = db.Column(db.String(10))
    earned_at  = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", foreign_keys=[user_id])
