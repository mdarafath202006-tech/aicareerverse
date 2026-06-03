"""app/models/community.py"""
from datetime import datetime
from .base import db


class Community(db.Model):
    __tablename__ = "communities"

    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(100), nullable=False, unique=True)
    slug        = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    icon        = db.Column(db.String(10), default="🌐")
    banner_url  = db.Column(db.String(500))
    created_by  = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    member_count = db.Column(db.Integer, default=0)
    post_count  = db.Column(db.Integer, default=0)
    is_active   = db.Column(db.Boolean, default=True)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    members = db.relationship("CommunityMember", backref="community", lazy="dynamic", cascade="all,delete")

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "slug": self.slug,
            "description": self.description, "icon": self.icon,
            "member_count": self.member_count, "post_count": self.post_count,
        }


class CommunityMember(db.Model):
    __tablename__ = "community_members"

    id           = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey("communities.id", ondelete="CASCADE"), nullable=False)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role         = db.Column(db.Enum("member","moderator","admin"), default="member")
    joined_at    = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("community_id", "user_id", name="uq_community_member"),)
