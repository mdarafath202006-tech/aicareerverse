"""app/models/alumni.py"""
from .base import db


class Alumni(db.Model):
    __tablename__ = "alumni"

    id                = db.Column(db.Integer, primary_key=True)
    user_id           = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    graduation_year   = db.Column(db.SmallInteger)
    company           = db.Column(db.String(150), index=True)
    job_role          = db.Column(db.String(150), index=True)
    skills            = db.Column(db.Text)
    location          = db.Column(db.String(100))
    linkedin          = db.Column(db.String(255))
    github_url        = db.Column(db.String(255))
    bio               = db.Column(db.Text)
    rating            = db.Column(db.Numeric(3, 2))
    mentorship_score  = db.Column(db.Integer, default=0)
    impact_score      = db.Column(db.Integer, default=0)
    is_hiring         = db.Column(db.Boolean, default=False)
    mentorship_slots  = db.Column(db.Integer, default=3)
    domain            = db.Column(db.String(100))
    skills_embedding  = db.Column(db.Text)  # JSON-encoded vector for FAISS/semantic search

    # Relationships
    mentorship_requests = db.relationship(
        "MentorshipRequest", backref="alumni",
        foreign_keys="MentorshipRequest.alumni_id",
        lazy="dynamic", cascade="all,delete"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "graduation_year": self.graduation_year,
            "company": self.company,
            "job_role": self.job_role,
            "skills": self.skills,
            "location": self.location,
            "linkedin": self.linkedin,
            "bio": self.bio,
            "rating": float(self.rating) if self.rating else None,
            "is_hiring": self.is_hiring,
            "mentorship_slots": self.mentorship_slots,
            "domain": self.domain,
        }

    def __repr__(self):
        return f"<Alumni {self.job_role} @ {self.company}>"
