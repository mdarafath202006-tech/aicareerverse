"""
tests/test_ai.py — AI recommender unit tests
"""
import pytest
from app.ai.recommender import (
    get_recommendations, get_skill_gap, get_career_analytics,
    _tokenize_skills, _skill_overlap,
)


STUDENT = {
    "skills": "Python, Machine Learning, React",
    "interests": "AI, Web Development",
    "department": "CSE",
}

ALUMNI = [
    {"id": 1, "name": "Alice", "skills": "Python, TensorFlow, ML", "job_role": "Data Scientist", "company": "Google", "bio": "ML engineer"},
    {"id": 2, "name": "Bob",   "skills": "React, JavaScript, Node", "job_role": "Frontend Engineer", "company": "Meta", "bio": ""},
    {"id": 3, "name": "Carol", "skills": "Java, Spring Boot",       "job_role": "Backend Engineer", "company": "Amazon", "bio": ""},
]


class TestTokenize:
    def test_basic(self):
        assert _tokenize_skills("Python, ML, React") == {"python", "ml", "react"}

    def test_semicolon(self):
        assert _tokenize_skills("Python; SQL") == {"python", "sql"}

    def test_empty(self):
        assert _tokenize_skills("") == set()

    def test_none(self):
        assert _tokenize_skills(None) == set()


class TestSkillOverlap:
    def test_overlap(self):
        score, matched = _skill_overlap(STUDENT, ALUMNI[0])
        assert score > 0
        assert "python" in matched

    def test_no_overlap(self):
        score, matched = _skill_overlap(STUDENT, ALUMNI[2])
        assert score == 0.0
        assert matched == []


class TestRecommendations:
    def test_returns_list(self):
        result = get_recommendations(STUDENT, ALUMNI)
        assert isinstance(result, list)

    def test_top_n(self):
        result = get_recommendations(STUDENT, ALUMNI, top_n=2)
        assert len(result) <= 2

    def test_has_required_keys(self):
        result = get_recommendations(STUDENT, ALUMNI)
        for r in result:
            assert "alumni"   in r
            assert "score"    in r
            assert "percent"  in r
            assert "matched_skills" in r

    def test_sorted_by_score(self):
        result = get_recommendations(STUDENT, ALUMNI)
        scores = [r["score"] for r in result]
        assert scores == sorted(scores, reverse=True)

    def test_empty_alumni(self):
        assert get_recommendations(STUDENT, []) == []


class TestSkillGap:
    def test_returns_dict(self):
        result = get_skill_gap(STUDENT, "Data Scientist", ALUMNI)
        assert isinstance(result, dict)
        assert "required_skills" in result
        assert "student_has"    in result
        assert "missing"        in result
        assert "coverage_pct"   in result

    def test_unknown_role(self):
        result = get_skill_gap(STUDENT, "NonExistentRole999", ALUMNI)
        assert result["coverage_pct"] == 0

    def test_coverage_range(self):
        result = get_skill_gap(STUDENT, "Data Scientist", ALUMNI)
        assert 0 <= result["coverage_pct"] <= 100


class TestAnalytics:
    def test_structure(self):
        data = get_career_analytics(ALUMNI)
        assert "top_companies" in data
        assert "top_roles"     in data
        assert "top_skills"    in data
        assert "by_year"       in data

    def test_empty_input(self):
        data = get_career_analytics([])
        assert data["top_companies"] == []
