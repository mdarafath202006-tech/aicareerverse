"""app/models/user.py"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from .base import db


class User(db.Model):
    __tablename__ = "users"

    id             = db.Column(db.Integer, primary_key=True)
    name           = db.Column(db.String(100), nullable=False)
    email          = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash  = db.Column("password", db.String(256), nullable=False)
    role           = db.Column(db.Enum("student", "alumni", "admin"), default="student", index=True)
    is_active      = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    avatar_url     = db.Column(db.String(500))
    cover_url      = db.Column(db.String(500))
    google_id      = db.Column(db.String(100), unique=True, nullable=True)
    linkedin_id    = db.Column(db.String(100), unique=True, nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    last_login     = db.Column(db.DateTime)

    # Relationships
    student     = db.relationship("Student", backref="user", uselist=False, cascade="all,delete")
    alumni      = db.relationship("Alumni",  backref="user", uselist=False, cascade="all,delete")
    posts       = db.relationship("Post", backref="author", lazy="dynamic")
    notifications = db.relationship("Notification", backref="recipient", lazy="dynamic")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "avatar_url": self.avatar_url,
            "email_verified": self.email_verified,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User {self.email}>"
