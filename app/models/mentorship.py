"""app/models/mentorship.py"""
from datetime import datetime
from .base import db


class MentorshipRequest(db.Model):
    __tablename__ = "mentorship_requests"

    id         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    alumni_id  = db.Column(db.Integer, db.ForeignKey("alumni.id",   ondelete="CASCADE"), nullable=False, index=True)
    message    = db.Column(db.Text)
    status     = db.Column(db.Enum("pending", "accepted", "rejected"), default="pending", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("student_id", "alumni_id", name="uq_request"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "alumni_id": self.alumni_id,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
