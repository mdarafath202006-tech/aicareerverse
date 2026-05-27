"""AI CareerVerse — Upgraded Configuration with PostgreSQL + Redis + Celery"""

import os
import datetime
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "aicareerverse-dev-secret-2025-change-in-prod"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-aicareerverse-secret"
    )

    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # ==============================
    # PostgreSQL Configuration
    # ==============================

    database_url = os.getenv("DATABASE_URL")

    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = (
        database_url or "sqlite:///aicareerverse.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20
    }

    # ==============================
    # Redis + Celery
    # ==============================

    REDIS_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    CELERY_BROKER_URL = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    CELERY_RESULT_BACKEND = os.getenv(
        "REDIS_URL",
        "redis://localhost:6379/0"
    )

    RATELIMIT_STORAGE_URL = os.getenv(
        "REDIS_URL",
        "memory://"
    )

    # ==============================
    # Cloudinary
    # ==============================

    CLOUDINARY_CLOUD_NAME = os.getenv(
        "CLOUDINARY_CLOUD_NAME",
        ""
    )

    CLOUDINARY_API_KEY = os.getenv(
        "CLOUDINARY_API_KEY",
        ""
    )

    CLOUDINARY_API_SECRET = os.getenv(
        "CLOUDINARY_API_SECRET",
        ""
    )

    # ==============================
    # Anthropic AI
    # ==============================

    ANTHROPIC_API_KEY = os.getenv(
        "ANTHROPIC_API_KEY",
        ""
    )

    # ==============================
    # OAuth
    # ==============================

    GOOGLE_CLIENT_ID = os.getenv(
        "GOOGLE_CLIENT_ID",
        ""
    )

    GOOGLE_CLIENT_SECRET = os.getenv(
        "GOOGLE_CLIENT_SECRET",
        ""
    )

    LINKEDIN_CLIENT_ID = os.getenv(
        "LINKEDIN_CLIENT_ID",
        ""
    )

    LINKEDIN_CLIENT_SECRET = os.getenv(
        "LINKEDIN_CLIENT_SECRET",
        ""
    )

    # ==============================
    # Email Configuration
    # ==============================

    MAIL_SERVER = os.getenv(
        "MAIL_SERVER",
        "smtp.gmail.com"
    )

    MAIL_PORT = int(
        os.getenv("MAIL_PORT", 587)
    )

    MAIL_USE_TLS = True

    MAIL_USERNAME = os.getenv(
        "MAIL_USERNAME",
        ""
    )

    MAIL_PASSWORD = os.getenv(
        "MAIL_PASSWORD",
        ""
    )


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    WTF_CSRF_ENABLED = True
