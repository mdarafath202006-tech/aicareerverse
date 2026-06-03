"""app/repositories/alumni_repo.py"""
from app.models import db, Alumni, User, MentorshipRequest


class AlumniRepository:

    @staticmethod
    def get_by_user_id(user_id: int) -> Alumni | None:
        return Alumni.query.filter_by(user_id=user_id).first()

    @staticmethod
    def get_all_with_users() -> list[dict]:
        rows = (
            db.session.query(Alumni, User)
            .join(User, Alumni.user_id == User.id)
            .filter(User.is_active == True)
            .all()
        )
        result = []
        for alum, user in rows:
            d = alum.to_dict()
            d["name"]      = user.name
            d["email"]     = user.email
            d["alumni_id"] = alum.id
            result.append(d)
        return result

    @staticmethod
    def get_by_id_with_user(alumni_id: int) -> dict | None:
        row = (
            db.session.query(Alumni, User)
            .join(User, Alumni.user_id == User.id)
            .filter(Alumni.id == alumni_id)
            .first()
        )
        if not row:
            return None
        alum, user = row
        d = alum.to_dict()
        d["name"]      = user.name
        d["email"]     = user.email
        d["alumni_id"] = alum.id
        return d

    @staticmethod
    def search(query: str = "", skill: str = "", company: str = "") -> list[dict]:
        q = db.session.query(Alumni, User).join(User, Alumni.user_id == User.id)
        if query:
            like = f"%{query}%"
            q = q.filter(
                db.or_(
                    User.name.ilike(like),
                    Alumni.job_role.ilike(like),
                    Alumni.skills.ilike(like),
                    Alumni.company.ilike(like),
                )
            )
        if skill:
            q = q.filter(Alumni.skills.ilike(f"%{skill}%"))
        if company:
            q = q.filter(Alumni.company.ilike(f"%{company}%"))
        results = []
        for alum, user in q.all():
            d = alum.to_dict()
            d["name"]      = user.name
            d["email"]     = user.email
            d["alumni_id"] = alum.id
            results.append(d)
        return results

    @staticmethod
    def get_pending_requests(alumni_id: int) -> list:
        from app.models import Student
        return (
            db.session.query(MentorshipRequest, Student, User)
            .join(Student, MentorshipRequest.student_id == Student.id)
            .join(User,    Student.user_id == User.id)
            .filter(MentorshipRequest.alumni_id == alumni_id)
            .order_by(MentorshipRequest.created_at.desc())
            .all()
        )

    @staticmethod
    def update_request_status(req_id: int, status: str):
        req = MentorshipRequest.query.get(req_id)
        if req:
            req.status = status
            db.session.commit()
        return req

    @staticmethod
    def distinct_roles() -> list[str]:
        rows = (db.session.query(Alumni.job_role)
                .filter(Alumni.job_role.isnot(None))
                .distinct()
                .order_by(Alumni.job_role)
                .all())
        return [r[0] for r in rows if r[0]]
