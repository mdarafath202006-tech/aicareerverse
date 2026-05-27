"""
app/models/__init__.py
SQLAlchemy ORM models — replacing raw mysql-connector-python.

Upgrade: Phase 2 — SQLAlchemy + Alembic
"""
from .base import db
from .user import User
from .student import Student
from .alumni import Alumni
from .mentorship import MentorshipRequest
from .post import Post
from .notification import Notification

__all__ = ["db", "User", "Student", "Alumni", "MentorshipRequest", "Post", "Notification"]
