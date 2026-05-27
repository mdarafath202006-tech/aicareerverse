"""app/models/post.py"""
from datetime import datetime
from .base import db


class Post(db.Model):
    __tablename__ = "posts"

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content        = db.Column(db.Text, nullable=False)
    image_url      = db.Column(db.String(500))
    post_type      = db.Column(db.Enum("text", "image", "video", "achievement", "job"), default="text")
    tags           = db.Column(db.String(500))
    likes_count    = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    shares_count   = db.Column(db.Integer, default=0)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "content": self.content,
            "post_type": self.post_type,
            "tags": self.tags,
            "likes_count": self.likes_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
