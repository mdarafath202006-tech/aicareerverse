"""tests/test_models.py — Model tests"""
import pytest
from app import create_app
from app.models.base import db as _db
from app.models import User, Student, Alumni, MentorshipRequest, Post


@pytest.fixture(scope="session")
def app():
    app = create_app("config.TestingConfig")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(autouse=True)
def clean_db(app):
    with app.app_context():
        yield
        _db.session.rollback()
        _db.session.query(MentorshipRequest).delete()
        _db.session.query(Post).delete()
        _db.session.query(Student).delete()
        _db.session.query(Alumni).delete()
        _db.session.query(User).delete()
        _db.session.commit()


def _make_student(email="s@test.com"):
    u = User(name="Student", email=email, role="student", is_active=True)
    u.set_password("Test@1234")
    _db.session.add(u); _db.session.flush()
    st = Student(user_id=u.id, department="CS", year="2nd",
                 skills="Python,React", interests="AI")
    _db.session.add(st); _db.session.commit()
    return u, st


def _make_alumni(email="a@test.com"):
    u = User(name="Alumni", email=email, role="alumni", is_active=True)
    u.set_password("Test@1234")
    _db.session.add(u); _db.session.flush()
    al = Alumni(user_id=u.id, company="Google",
                job_role="SWE", skills="Python,Go", mentorship_slots=3)
    _db.session.add(al); _db.session.commit()
    return u, al


def test_create_user(app):
    with app.app_context():
        u = User(name="Test", email="t@test.com", role="student", is_active=True)
        u.set_password("Test@1234")
        _db.session.add(u); _db.session.commit()
        found = User.query.filter_by(email="t@test.com").first()
        assert found is not None
        assert found.name == "Test"


def test_password_hash(app):
    with app.app_context():
        u = User(name="PW", email="pw@test.com", role="student", is_active=True)
        u.set_password("SecurePass1")
        assert u.check_password("SecurePass1")
        assert not u.check_password("wrongpassword")


def test_create_student(app):
    with app.app_context():
        _, st = _make_student()
        assert st.department == "CS"
        assert "Python" in st.skills


def test_create_alumni(app):
    with app.app_context():
        _, al = _make_alumni()
        assert al.company == "Google"
        assert al.mentorship_slots == 3


def test_mentorship_request(app):
    with app.app_context():
        _, st = _make_student("ms@test.com")
        _, al = _make_alumni("ma@test.com")
        req = MentorshipRequest(
            student_id=st.id, alumni_id=al.id,
            message="Please mentor me", status="pending",
        )
        _db.session.add(req); _db.session.commit()
        found = MentorshipRequest.query.filter_by(
            student_id=st.id, alumni_id=al.id).first()
        assert found is not None
        assert found.status == "pending"


def test_post_create(app):
    with app.app_context():
        u, _ = _make_student("post@test.com")
        post = Post(user_id=u.id, content="Hello world", post_type="text")
        _db.session.add(post); _db.session.commit()
        found = Post.query.filter_by(user_id=u.id).first()
        assert found is not None
        assert found.content == "Hello world"


def test_alumni_to_dict(app):
    with app.app_context():
        _, al = _make_alumni("dict@test.com")
        d = al.to_dict()
        assert "company" in d
        assert d["company"] == "Google"


def test_user_to_dict(app):
    with app.app_context():
        u, _ = _make_student("ud@test.com")
        d = u.to_dict()
        assert d["role"] == "student"
        assert "email" in d
