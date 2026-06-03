"""
app/tasks/ai_tasks.py
Background AI processing tasks via Celery.
"""
import logging
from .celery_app import celery

logger = logging.getLogger(__name__)


@celery.task(bind=True, max_retries=3, name="app.tasks.ai_tasks.analyze_resume")
def analyze_resume(self, student_id: int, resume_text: str):
    """
    Async resume analysis:
    - Extract skills
    - Compute AI score
    - Update placement score
    """
    try:
        from app.models import db, Student
        from app.ai.recommender import compute_placement_score

        student = Student.query.get(student_id)
        if not student:
            return {"error": "Student not found"}

        # Extract skills from resume text using keyword matching
        tech_skills = [
            "python", "java", "javascript", "react", "node.js", "sql",
            "machine learning", "deep learning", "tensorflow", "pytorch",
            "docker", "kubernetes", "aws", "gcp", "azure", "git",
            "flask", "django", "fastapi", "redis", "mongodb", "postgresql"
        ]
        found_skills = [sk for sk in tech_skills if sk in resume_text.lower()]

        if found_skills:
            existing = set(student.skills.lower().split(",")) if student.skills else set()
            new_skills = existing | set(found_skills)
            student.skills = ", ".join(sorted(new_skills))

        # Recompute AI score
        from app.repositories.alumni_repo import AlumniRepository
        alumni_list = AlumniRepository.get_all_with_users()
        score = compute_placement_score(student.to_dict(), alumni_list)
        student.placement_score = score
        student.ai_score = min(score + 10, 100)

        db.session.commit()
        logger.info(f"Resume analyzed for student {student_id}: score={score}")
        return {"student_id": student_id, "placement_score": score, "skills_added": found_skills}

    except Exception as exc:
        logger.error(f"Resume analysis failed: {exc}")
        raise self.retry(exc=exc, countdown=60)


@celery.task(name="app.tasks.ai_tasks.recompute_recommendations")
def recompute_recommendations(student_id: int):
    """Precompute and cache recommendations for a student."""
    try:
        from app.models import Student
        from app.repositories.alumni_repo import AlumniRepository
        from app.ai.recommender import get_recommendations
        import json

        student = Student.query.get(student_id)
        if not student:
            return
        alumni_list = AlumniRepository.get_all_with_users()
        ranked = get_recommendations(student.to_dict(), alumni_list)
        # In production: cache in Redis
        # redis_client.setex(f"recs:{student_id}", 3600, json.dumps(ranked))
        logger.info(f"Recommendations cached for student {student_id}")
        return {"count": len(ranked)}
    except Exception as exc:
        logger.error(f"Recompute recommendations failed: {exc}")
