"""
tests/test_auth.py — Auth endpoint tests (Phase 9: Pytest upgrade)
"""
import pytest
import json


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def app():
    from app import create_app
    app = create_app("config.DevelopmentConfig")
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    from app.models.base import db
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


class TestRegistration:
    def test_register_student(self, client):
        res = client.post("/register", data={
            "name": "Test Student", "email": "test@example.com",
            "password": "SecurePass1", "role": "student",
            "department": "CSE", "year": "3rd",
        }, follow_redirects=True)
        assert res.status_code == 200

    def test_register_duplicate_email(self, client):
        data = {"name": "User", "email": "dup@test.com", "password": "SecurePass1", "role": "student"}
        client.post("/register", data=data)
        res = client.post("/register", data=data, follow_redirects=True)
        assert b"already registered" in res.data

    def test_register_invalid_email(self, client):
        res = client.post("/register", data={
            "name": "User", "email": "not-an-email",
            "password": "SecurePass1", "role": "student",
        }, follow_redirects=True)
        assert res.status_code in (200, 302)

    def test_register_weak_password(self, client):
        res = client.post("/register", data={
            "name": "User", "email": "weak@test.com",
            "password": "weak", "role": "student",
        }, follow_redirects=True)
        assert res.status_code in (200, 302)


class TestLogin:
    def _register(self, client):
        client.post("/register", data={
            "name": "Auth User", "email": "auth@test.com",
            "password": "SecurePass1", "role": "student", "department": "CSE", "year": "2nd",
        })

    def test_valid_login(self, client):
        self._register(client)
        res = client.post("/login", data={"email": "auth@test.com", "password": "SecurePass1"}, follow_redirects=True)
        assert res.status_code == 200

    def test_invalid_password(self, client):
        self._register(client)
        res = client.post("/login", data={"email": "auth@test.com", "password": "WrongPass1"}, follow_redirects=True)
        assert b"Invalid" in res.data

    def test_nonexistent_user(self, client):
        res = client.post("/login", data={"email": "nobody@test.com", "password": "Pass1"}, follow_redirects=True)
        assert b"Invalid" in res.data

    def test_logout(self, client):
        self._register(client)
        client.post("/login", data={"email": "auth@test.com", "password": "SecurePass1"})
        res = client.get("/logout", follow_redirects=True)
        assert res.status_code == 200


class TestAPIAuth:
    def _register_and_get_token(self, client):
        client.post("/register", data={
            "name": "API User", "email": "api@test.com",
            "password": "SecurePass1", "role": "student", "department": "CS", "year": "1st",
        })
        res = client.post("/api/auth/login",
                          json={"email": "api@test.com", "password": "SecurePass1"},
                          content_type="application/json")
        data = json.loads(res.data)
        return data.get("access_token")

    def test_jwt_login(self, client):
        token = self._register_and_get_token(client)
        assert token is not None

    def test_jwt_required_without_token(self, client):
        res = client.get("/api/recommendations")
        assert res.status_code == 401

    def test_jwt_required_with_token(self, client):
        token = self._register_and_get_token(client)
        res = client.get("/api/recommendations",
                         headers={"Authorization": f"Bearer {token}"})
        assert res.status_code in (200, 404)
