"""app/models/student.py"""
from .base import db


class Student(db.Model):
    __tablename__ = "students"

    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"),
                            unique=True, nullable=False)
    department  = db.Column(db.String(100))
    year        = db.Column(db.String(20))
    skills      = db.Column(db.Text)
    interests   = db.Column(db.Text)
    bio         = db.Column(db.Text)
    resume_url  = db.Column(db.String(500))
    github_url  = db.Column(db.String(255))
    linkedin_url = db.Column(db.String(255))

    mentorship_requests = db.relationship(
        "MentorshipRequest", backref="student",
        foreign_keys="MentorshipRequest.student_id",
        lazy="dynamic", cascade="all,delete",
    )

    def to_dict(self):
        return {
            "id":           self.id,
            "user_id":      self.user_id,
            "department":   self.department,
            "year":         self.year,
            "skills":       self.skills,
            "interests":    self.interests,
            "bio":          self.bio,
            "resume_url":   self.resume_url,
            "github_url":   self.github_url,
            "linkedin_url": self.linkedin_url,
        }

    def __repr__(self):
        return f"<Student {self.department} yr{self.year}>"
