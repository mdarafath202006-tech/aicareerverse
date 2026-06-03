"""app/models/knowledge.py — Knowledge Base (Alumni Stories / Interview Experiences)"""
from datetime import datetime
from .base import db


class KnowledgeEntry(db.Model):
    __tablename__ = "knowledge_entries"

    id           = db.Column(db.Integer, primary_key=True)
    author_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title        = db.Column(db.String(300), nullable=False)
    category     = db.Column(db.Enum(
        "success_story", "interview_experience", "placement_story",
        "career_guide", "company_review", "tips_and_tricks"
    ), default="career_guide")
    content      = db.Column(db.Text, nullable=False)
    company      = db.Column(db.String(150))
    role         = db.Column(db.String(150))
    tags         = db.Column(db.String(500))
    is_approved  = db.Column(db.Boolean, default=True)
    views        = db.Column(db.Integer, default=0)
    helpful_count = db.Column(db.Integer, default=0)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("User", foreign_keys=[author_id])

    def to_dict(self):
        return {
            "id": self.id, "title": self.title, "category": self.category,
            "content": self.content, "company": self.company, "role": self.role,
            "tags": self.tags, "views": self.views, "helpful_count": self.helpful_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
