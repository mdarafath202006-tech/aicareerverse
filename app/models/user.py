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
    role           = db.Column(db.Enum("student", "alumni", "mentor", "recruiter", "admin"), default="student", index=True)
    is_active      = db.Column(db.Boolean, default=True)
    email_verified = db.Column(db.Boolean, default=False)
    avatar_url     = db.Column(db.String(500))
    cover_url      = db.Column(db.String(500))
    google_id      = db.Column(db.String(100), unique=True, nullable=True)
    linkedin_id    = db.Column(db.String(100), unique=True, nullable=True)
    created_at     = db.Column(db.DateTime, default=datetime.utcnow)
    last_login     = db.Column(db.DateTime)

    # Relationships
    student       = db.relationship("Student", backref="user", uselist=False, cascade="all,delete")
    alumni        = db.relationship("Alumni",  backref="user", uselist=False, cascade="all,delete")
    posts         = db.relationship("Post", backref="author", lazy="dynamic")
    notifications = db.relationship("Notification", backref="recipient", lazy="dynamic")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def profile_completion(self):
        """Returns 0-100 profile completion score."""
        score = 20  # base
        if self.avatar_url:  score += 15
        if self.cover_url:   score += 5
        if self.student:
            s = self.student
            if s.bio:         score += 15
            if s.skills:      score += 15
            if s.department:  score += 10
            if s.resume_url:  score += 15
            if s.github_url:  score += 5
        elif self.alumni:
            a = self.alumni
            if a.bio:         score += 15
            if a.skills:      score += 15
            if a.company:     score += 10
            if a.linkedin:    score += 10
            if a.location:    score += 5
        return min(score, 100)

    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "email": self.email,
            "role": self.role, "avatar_url": self.avatar_url,
            "email_verified": self.email_verified,
            "profile_completion": self.profile_completion(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<User {self.email}>"
