"""
app/repositories/student_repo.py
Repository pattern — keeps route handlers thin and testable.
"""
from app.models import db, Student, User, MentorshipRequest


class StudentRepository:

    @staticmethod
    def get_by_user_id(user_id: int) -> Student | None:
        return Student.query.filter_by(user_id=user_id).first()

    @staticmethod
    def update_profile(student: Student, **kwargs) -> Student:
        for key, value in kwargs.items():
            if hasattr(student, key):
                setattr(student, key, value)
        db.session.commit()
        return student

    @staticmethod
    def get_stats(student_id: int) -> dict:
        req_count = MentorshipRequest.query.filter_by(student_id=student_id).count()
        accepted  = MentorshipRequest.query.filter_by(
            student_id=student_id, status="accepted"
        ).count()
        alumni_count = User.query.filter_by(role="alumni").count()
        return {
            "req_count": req_count,
            "accepted_count": accepted,
            "alumni_count": alumni_count,
        }

    @staticmethod
    def has_pending_request(student_id: int, alumni_id: int) -> bool:
        return MentorshipRequest.query.filter_by(
            student_id=student_id,
            alumni_id=alumni_id,
            status="pending"
        ).first() is not None

    @staticmethod
    def send_request(student_id: int, alumni_id: int, message: str) -> MentorshipRequest:
        req = MentorshipRequest(
            student_id=student_id,
            alumni_id=alumni_id,
            message=message
        )
        db.session.add(req)
        db.session.commit()
        return req
