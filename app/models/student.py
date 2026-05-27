"""app/models/student.py"""
from .base import db


class Student(db.Model):
    __tablename__ = "students"

    id               = db.Column(db.Integer, primary_key=True)
    user_id          = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    department       = db.Column(db.String(100))
    year             = db.Column(db.String(10))
    skills           = db.Column(db.Text)
    interests        = db.Column(db.Text)
    bio              = db.Column(db.Text)
    github_url       = db.Column(db.String(255))
    linkedin_url     = db.Column(db.String(255))
    resume_url       = db.Column(db.String(500))
    ai_score         = db.Column(db.Integer, default=0)
    placement_score  = db.Column(db.Integer, default=0)
    # Embedding vector stored as JSON string for semantic search
    skills_embedding = db.Column(db.Text)

    # Relationships
    mentorship_requests = db.relationship(
        "MentorshipRequest", backref="student",
        foreign_keys="MentorshipRequest.student_id",
        lazy="dynamic", cascade="all,delete"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "department": self.department,
            "year": self.year,
            "skills": self.skills,
            "interests": self.interests,
            "bio": self.bio,
            "github_url": self.github_url,
            "linkedin_url": self.linkedin_url,
            "resume_url": self.resume_url,
            "ai_score": self.ai_score,
            "placement_score": self.placement_score,
        }

    def __repr__(self):
        return f"<Student user_id={self.user_id}>"
