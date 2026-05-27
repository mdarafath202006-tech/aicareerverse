"""
app/tasks/notification_tasks.py
Real-time notification delivery via Celery + Socket.IO.
"""
import logging
from .celery_app import celery

logger = logging.getLogger(__name__)


@celery.task(name="app.tasks.notification_tasks.send_mentor_accepted")
def send_mentor_accepted(student_user_id: int, alumni_name: str, request_id: int):
    """Notify student that a mentor accepted their request."""
    try:
        from app.models import db, Notification
        notif = Notification(
            user_id=student_user_id,
            type="mentor_accepted",
            title="Mentor Request Accepted! 🎉",
            message=f"{alumni_name} accepted your mentorship request.",
            link=f"/student/dashboard",
        )
        db.session.add(notif)
        db.session.commit()
        logger.info(f"Notification sent to user {student_user_id}")
    except Exception as exc:
        logger.error(f"Notification task failed: {exc}")


@celery.task(name="app.tasks.notification_tasks.send_mentor_request_alert")
def send_mentor_request_alert(alumni_user_id: int, student_name: str):
    """Notify alumni of a new mentorship request."""
    try:
        from app.models import db, Notification
        notif = Notification(
            user_id=alumni_user_id,
            type="mentor_request",
            title="New Mentorship Request",
            message=f"{student_name} wants you as their mentor.",
            link="/alumni/dashboard",
        )
        db.session.add(notif)
        db.session.commit()
    except Exception as exc:
        logger.error(f"Alert task failed: {exc}")


@celery.task(name="app.tasks.notification_tasks.send_placement_alert")
def send_placement_alert(student_user_id: int, company: str, job_role: str):
    """Notify student of a relevant job opening."""
    try:
        from app.models import db, Notification
        notif = Notification(
            user_id=student_user_id,
            type="placement_alert",
            title=f"Job Opening: {job_role}",
            message=f"{company} is hiring for {job_role}. Your profile is a match!",
            link="/student/search",
        )
        db.session.add(notif)
        db.session.commit()
    except Exception as exc:
        logger.error(f"Placement alert failed: {exc}")
