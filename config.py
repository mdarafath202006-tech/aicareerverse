"""AI CareerVerse V3 — Configuration (PostgreSQL / Neon)"""
import os, datetime
from dotenv import load_dotenv
load_dotenv()


class BaseConfig:
    SECRET_KEY               = os.getenv("SECRET_KEY", "aicareerverse-dev-secret-v3-change-in-prod")
    JWT_SECRET_KEY           = os.getenv("JWT_SECRET_KEY", "jwt-aicareerverse-secret-v3")
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    WTF_CSRF_ENABLED         = True
    WTF_CSRF_TIME_LIMIT      = 3600
    SESSION_COOKIE_HTTPONLY  = True
    SESSION_COOKIE_SAMESITE  = "Lax"
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=7)
    MAX_CONTENT_LENGTH       = 16 * 1024 * 1024  # 16 MB

    # ── PostgreSQL (Neon / Render / local) ─────────────────────────────────
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:password@localhost:5432/aicareerverse"
    )
    # Neon uses "postgres://" prefix — normalise for SQLAlchemy
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
        "pool_size": 10,
        "max_overflow": 20,
    }

    # ── Redis / Celery ──────────────────────────────────────────────────────
    REDIS_URL             = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_BROKER_URL     = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    RATELIMIT_STORAGE_URL = os.getenv("REDIS_URL", "memory://")

    # ── Cloudinary ──────────────────────────────────────────────────────────
    CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
    CLOUDINARY_API_KEY    = os.getenv("CLOUDINARY_API_KEY", "")
    CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

    # ── AI ──────────────────────────────────────────────────────────────────
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

    # ── OAuth ────────────────────────────────────────────────────────────────
    GOOGLE_CLIENT_ID       = os.getenv("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET   = os.getenv("GOOGLE_CLIENT_SECRET", "")
    LINKEDIN_CLIENT_ID     = os.getenv("LINKEDIN_CLIENT_ID", "")
    LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")

    # ── Email ────────────────────────────────────────────────────────────────
    MAIL_SERVER   = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT     = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    WTF_CSRF_ENABLED = True


class TestingConfig(BaseConfig):
    TESTING          = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    DEBUG            = False
    WTF_CSRF_ENABLED = True
    SESSION_COOKIE_SECURE = True
