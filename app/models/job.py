"""app/models/job.py"""
from datetime import datetime
from .base import db


class Job(db.Model):
    __tablename__ = "jobs"

    id           = db.Column(db.Integer, primary_key=True)
    posted_by    = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title        = db.Column(db.String(200), nullable=False)
    company      = db.Column(db.String(150), nullable=False)
    location     = db.Column(db.String(150))
    job_type     = db.Column(db.Enum("full_time","internship","part_time","contract"), default="full_time")
    description  = db.Column(db.Text)
    requirements = db.Column(db.Text)
    skills_required = db.Column(db.String(500))
    salary_range = db.Column(db.String(100))
    apply_url    = db.Column(db.String(500))
    is_active    = db.Column(db.Boolean, default=True)
    views        = db.Column(db.Integer, default=0)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)
    deadline     = db.Column(db.DateTime)

    applications = db.relationship("JobApplication", backref="job", lazy="dynamic", cascade="all,delete")
    poster       = db.relationship("User", foreign_keys=[posted_by])

    def to_dict(self):
        return {
            "id": self.id, "title": self.title, "company": self.company,
            "location": self.location, "job_type": self.job_type,
            "description": self.description, "salary_range": self.salary_range,
            "skills_required": self.skills_required, "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class JobApplication(db.Model):
    __tablename__ = "job_applications"

    id           = db.Column(db.Integer, primary_key=True)
    job_id       = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    user_id      = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    status       = db.Column(db.Enum("applied","shortlisted","rejected","hired"), default="applied")
    cover_letter = db.Column(db.Text)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("job_id", "user_id", name="uq_job_application"),)
