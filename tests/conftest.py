"""tests/conftest.py — shared pytest fixtures"""
import pytest

@pytest.fixture(scope="session")
def app():
    from app import create_app
    application = create_app("config.DevelopmentConfig")
    application.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SERVER_NAME": "localhost",
    })
    from app.models.base import db
    with application.app_context():
        db.create_all()
        yield application
        db.drop_all()

@pytest.fixture(scope="session")
def client(app):
    return app.test_client()
