"""app/models/post.py — Extended with Comments and Likes"""
from datetime import datetime
from .base import db


class Post(db.Model):
    __tablename__ = "posts"

    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content        = db.Column(db.Text, nullable=False)
    image_url      = db.Column(db.String(500))
    post_type      = db.Column(db.Enum("text","image","achievement","opportunity","project"), default="text")
    tags           = db.Column(db.String(500))
    likes_count    = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    shares_count   = db.Column(db.Integer, default=0)
    is_pinned      = db.Column(db.Boolean, default=False)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    comments = db.relationship("Comment", backref="post", lazy="dynamic", cascade="all,delete")
    likes    = db.relationship("Like", backref="post", lazy="dynamic", cascade="all,delete")

    def to_dict(self):
        return {
            "id": self.id, "user_id": self.user_id,
            "content": self.content, "post_type": self.post_type,
            "tags": self.tags, "likes_count": self.likes_count,
            "comments_count": self.comments_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Comment(db.Model):
    __tablename__ = "comments"

    id         = db.Column(db.Integer, primary_key=True)
    post_id    = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content    = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    author = db.relationship("User", foreign_keys=[user_id])


class Like(db.Model):
    __tablename__ = "likes"

    id         = db.Column(db.Integer, primary_key=True)
    post_id    = db.Column(db.Integer, db.ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("post_id", "user_id", name="uq_like"),)
