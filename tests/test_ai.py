"""tests/test_ai.py — AI Recommender & Skill Gap tests"""
import pytest
from app.ai.recommender import (
    get_recommendations, get_skill_gap, get_career_analytics,
    _tokenize_skills, _skill_overlap,
)

ALUMNI_LIST = [
    {"id": 1, "name": "A", "job_role": "ML Engineer",     "company": "Google",
     "skills": "Python,TensorFlow,PyTorch,MLOps", "bio": "ML at Google"},
    {"id": 2, "name": "B", "job_role": "Software Engineer", "company": "Microsoft",
     "skills": "C#,.NET,Azure,System Design",     "bio": "Backend at MSFT"},
    {"id": 3, "name": "C", "job_role": "Data Scientist",   "company": "Amazon",
     "skills": "Python,SQL,Spark,Statistics",      "bio": "Data at Amazon"},
]

STUDENT = {
    "skills": "Python,TensorFlow,Machine Learning",
    "interests": "AI,Research",
    "department": "CS",
}


def test_recommendations_returns_list():
    result = get_recommendations(STUDENT, ALUMNI_LIST)
    assert isinstance(result, list)
    assert len(result) <= 10


def test_recommendations_sorted_by_score():
    result = get_recommendations(STUDENT, ALUMNI_LIST)
    scores = [r["score"] for r in result]
    assert scores == sorted(scores, reverse=True)


def test_recommendations_has_required_keys():
    result = get_recommendations(STUDENT, ALUMNI_LIST)
    for r in result:
        assert "alumni" in r
        assert "score" in r
        assert "percent" in r
        assert "matched_skills" in r


def test_ml_engineer_ranks_highest():
    result = get_recommendations(STUDENT, ALUMNI_LIST)
    if result:
        top = result[0]["alumni"]
        assert top["job_role"] in ("ML Engineer", "Data Scientist")


def test_recommendations_empty_alumni():
    result = get_recommendations(STUDENT, [])
    assert result == []


def test_skill_gap_returns_dict():
    gap = get_skill_gap(STUDENT, "ML Engineer", ALUMNI_LIST)
    assert isinstance(gap, dict)
    assert "missing" in gap
    assert "student_has" in gap


def test_skill_gap_coverage_pct():
    gap = get_skill_gap(STUDENT, "ML Engineer", ALUMNI_LIST)
    assert 0 <= gap.get("coverage_pct", 0) <= 100


def test_skill_gap_no_relevant_alumni():
    gap = get_skill_gap(STUDENT, "Quantum Physicist", ALUMNI_LIST)
    assert gap.get("missing", []) == []


def test_tokenize_skills():
    tokens = _tokenize_skills("Python, React, Machine Learning; SQL")
    assert "python" in tokens
    assert "react" in tokens
    assert "sql" in tokens


def test_skill_overlap():
    s = {"skills": "Python,React,SQL", "interests": "AI"}
    a = {"skills": "Python,Go,SQL,Docker"}
    overlap, matched = _skill_overlap(s, a)
    assert 0 < overlap <= 1
    assert "python" in matched
    assert "sql" in matched


def test_career_analytics_structure():
    data = get_career_analytics(ALUMNI_LIST)
    assert "top_companies"  in data
    assert "top_roles"      in data
    assert "top_skills"     in data
    assert "total_alumni"   in data
    assert data["total_alumni"] == 3


def test_percent_bounded():
    result = get_recommendations(STUDENT, ALUMNI_LIST)
    for r in result:
        assert 0 <= r["percent"] <= 99
