"""app/models/referral.py — Referral System"""
from datetime import datetime
from .base import db


class Referral(db.Model):
    __tablename__ = "referrals"

    id          = db.Column(db.Integer, primary_key=True)
    student_id  = db.Column(db.Integer, db.ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True)
    alumni_id   = db.Column(db.Integer, db.ForeignKey("alumni.id", ondelete="CASCADE"), nullable=False, index=True)
    job_id      = db.Column(db.Integer, db.ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True)
    company     = db.Column(db.String(150))
    position    = db.Column(db.String(150))
    message     = db.Column(db.Text)
    status      = db.Column(db.Enum("pending", "approved", "rejected"), default="pending", nullable=False)
    alumni_note = db.Column(db.Text)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    student = db.relationship("Student", foreign_keys=[student_id], backref=db.backref("referrals", lazy="dynamic"))
    alumni  = db.relationship("Alumni",  foreign_keys=[alumni_id],  backref=db.backref("referrals_given", lazy="dynamic"))

    def to_dict(self):
        return {
            "id":          self.id,
            "student_id":  self.student_id,
            "alumni_id":   self.alumni_id,
            "company":     self.company,
            "position":    self.position,
            "message":     self.message,
            "status":      self.status,
            "alumni_note": self.alumni_note,
            "created_at":  self.created_at.isoformat() if self.created_at else None,
        }
