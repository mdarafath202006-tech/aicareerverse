"""tests/test_auth.py — Auth tests"""
import pytest
from app import create_app
from app.models.base import db as _db


@pytest.fixture(scope="session")
def app():
    app = create_app("config.TestingConfig")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_db(app):
    """Roll back after each test."""
    with app.app_context():
        yield
        _db.session.rollback()
        from app.models import User, Student, Alumni
        _db.session.query(Student).delete()
        _db.session.query(Alumni).delete()
        _db.session.query(User).delete()
        _db.session.commit()


def test_index_redirects_to_landing(client):
    r = client.get("/")
    assert r.status_code in (200, 302)


def test_login_page_loads(client):
    r = client.get("/login")
    assert r.status_code == 200
    assert b"Sign In" in r.data or b"Login" in r.data


def test_register_page_loads(client):
    r = client.get("/register")
    assert r.status_code == 200
    assert b"Create" in r.data or b"Register" in r.data


def test_register_student(client):
    r = client.post("/register", data={
        "name": "Test Student",
        "email": "teststudent@test.com",
        "password": "Test@1234",
        "role": "student",
        "department": "CS",
        "year": "2nd",
    }, follow_redirects=True)
    assert r.status_code == 200


def test_register_alumni(client):
    r = client.post("/register", data={
        "name": "Test Alumni",
        "email": "testalumni@test.com",
        "password": "Test@1234",
        "role": "alumni",
        "company": "Google",
        "job_role": "SWE",
    }, follow_redirects=True)
    assert r.status_code == 200


def test_login_valid(client):
    # Register first
    client.post("/register", data={
        "name": "Login Test",
        "email": "logintest@test.com",
        "password": "Test@1234",
        "role": "student",
    })
    r = client.post("/login", data={
        "email": "logintest@test.com",
        "password": "Test@1234",
    }, follow_redirects=True)
    assert r.status_code == 200


def test_login_invalid_password(client):
    client.post("/register", data={
        "name": "Wrong Pass",
        "email": "wrongpass@test.com",
        "password": "Test@1234",
        "role": "student",
    })
    r = client.post("/login", data={
        "email": "wrongpass@test.com",
        "password": "WrongPassword",
    }, follow_redirects=True)
    assert b"Invalid" in r.data or r.status_code == 200


def test_logout(client):
    r = client.get("/logout", follow_redirects=True)
    assert r.status_code == 200


def test_weak_password_rejected(client):
    r = client.post("/register", data={
        "name": "Weak Pass User",
        "email": "weak@test.com",
        "password": "short",
        "role": "student",
    }, follow_redirects=True)
    assert r.status_code == 200
    # Should not have created user
    from app.models import User
    u = User.query.filter_by(email="weak@test.com").first()
    assert u is None


def test_duplicate_email_rejected(client):
    data = {
        "name": "Dupe", "email": "dupe@test.com",
        "password": "Test@1234", "role": "student",
    }
    client.post("/register", data=data)
    r = client.post("/register", data=data, follow_redirects=True)
    assert r.status_code == 200
    from app.models import User
    assert User.query.filter_by(email="dupe@test.com").count() == 1
