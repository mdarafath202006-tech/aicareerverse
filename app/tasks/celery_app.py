"""
app/tasks/celery_app.py
Celery + Redis setup for async task processing.

Phase 4 Upgrade: Background tasks for:
  - Resume analysis
  - Email notifications
  - AI score computation
  - Placement alerts
"""
from celery import Celery
import os


def make_celery(app=None):
    broker  = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    celery = Celery(
        "aicareerverse",
        broker=broker,
        backend=backend,
        include=["app.tasks.ai_tasks", "app.tasks.notification_tasks"],
    )

    celery.conf.update(
        task_serializer="json",
        accept_content=["json"],
        result_serializer="json",
        timezone="UTC",
        enable_utc=True,
        task_routes={
            "app.tasks.ai_tasks.*":           {"queue": "ai"},
            "app.tasks.notification_tasks.*": {"queue": "notifications"},
        },
    )

    if app:
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)
        celery.Task = ContextTask

    return celery


celery = make_celery()
