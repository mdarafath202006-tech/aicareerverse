"""app/models/project.py"""
from datetime import datetime
from .base import db


class ProjectShowcase(db.Model):
    __tablename__ = "project_showcases"

    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    description  = db.Column(db.Text)
    tech_stack   = db.Column(db.String(500))
    github_url   = db.Column(db.String(500))
    demo_url     = db.Column(db.String(500))
    image_url    = db.Column(db.String(500))
    likes_count  = db.Column(db.Integer, default=0)
    views        = db.Column(db.Integer, default=0)
    is_featured  = db.Column(db.Boolean, default=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("User", foreign_keys=[user_id])

    def to_dict(self):
        return {
            "id": self.id, "title": self.title, "description": self.description,
            "tech_stack": self.tech_stack, "github_url": self.github_url,
            "demo_url": self.demo_url, "likes_count": self.likes_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
