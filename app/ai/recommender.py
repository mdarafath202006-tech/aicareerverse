"""
app/ai/recommender.py — Upgraded AI Engine

Phase 3 Upgrades:
  ✅ Semantic embeddings via SentenceTransformers (or fallback to TF-IDF)
  ✅ Vector similarity search (FAISS-compatible cosine)
  ✅ Composite scoring: semantic + keyword overlap + industry alignment
  ✅ RAG-style mentor matching
  ✅ Placement prediction scoring
  ✅ Skill gap with learning paths
"""
import re
import logging
from collections import Counter

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

_embedder = None
try:
    from sentence_transformers import SentenceTransformer
    _embedder = SentenceTransformer("all-MiniLM-L6-v2")
    logger.info("SentenceTransformers loaded — semantic search enabled.")
except ImportError:
    logger.warning("SentenceTransformers not installed — falling back to TF-IDF.")

WEIGHTS = {"semantic": 0.50, "skill": 0.35, "industry": 0.15}


def _tokenize_skills(text):
    if not text:
        return set()
    return {s.strip().lower() for s in re.split(r"[,;|]+", text) if s.strip()}


def _build_text(record, fields):
    return " ".join(str(record.get(f) or "").lower().strip() for f in fields)


def _skill_overlap(student, alumnus):
    s_set = _tokenize_skills(student.get("skills", "")) | _tokenize_skills(student.get("interests", ""))
    a_set = _tokenize_skills(alumnus.get("skills", ""))
    if not s_set or not a_set:
        return 0.0, []
    inter = s_set & a_set
    union = s_set | a_set
    return len(inter) / len(union), sorted(inter)


def _industry_score(student, alumnus):
    dept = (student.get("department") or "").lower()
    role = (alumnus.get("job_role") or "").lower()
    bio  = (alumnus.get("bio") or "").lower()
    cs_kw   = {"cse", "cs", "computer", "it", "software", "data", "ai", "ml"}
    tech_kw = {"software", "data", "ai", "ml", "engineer", "developer", "analyst", "cloud", "cyber"}
    if dept and any(k in dept for k in cs_kw):
        if any(k in role or k in bio for k in tech_kw):
            return 1.0
    if dept and dept.split()[0] in role:
        return 0.6
    return 0.0


def _cosine(a, b):
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom else 0.0


def get_recommendations(student, alumni_list, top_n=10):
    if not alumni_list:
        return []
    student_text = _build_text(student, ["skills", "interests", "department"])
    alumni_texts = [_build_text(a, ["skills", "job_role", "company", "bio"]) for a in alumni_list]

    if _embedder is not None:
        try:
            student_emb = _embedder.encode(student_text, show_progress_bar=False)
            alumni_embs = _embedder.encode(alumni_texts, show_progress_bar=False)
            semantic_scores = [_cosine(student_emb, e) for e in alumni_embs]
        except Exception:
            semantic_scores = _tfidf_scores(student_text, alumni_texts)
    else:
        semantic_scores = _tfidf_scores(student_text, alumni_texts)

    results = []
    for i, alumnus in enumerate(alumni_list):
        sem_s            = float(semantic_scores[i])
        skill_s, matched = _skill_overlap(student, alumnus)
        ind_s            = _industry_score(student, alumnus)
        composite = WEIGHTS["semantic"]*sem_s + WEIGHTS["skill"]*skill_s + WEIGHTS["industry"]*ind_s
        results.append({
            "alumni":         alumnus,
            "score":          round(composite, 4),
            "percent":        min(int(composite * 100), 99),
            "skill_overlap":  int(skill_s * 100),
            "matched_skills": matched,
            "semantic_score": round(sem_s, 3),
        })
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_n]


def _tfidf_scores(student_text, alumni_texts):
    all_texts = [student_text] + alumni_texts
    vec = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
    try:
        mat = vec.fit_transform(all_texts)
        return cosine_similarity(mat[0], mat[1:]).flatten().tolist()
    except ValueError:
        return [0.0] * len(alumni_texts)


def get_career_analytics(alumni_data):
    companies, roles, skills_all, years = [], [], [], []
    for a in alumni_data:
        if a.get("company"):    companies.append(a["company"].strip().title())
        if a.get("job_role"):   roles.append(a["job_role"].strip().title())
        if a.get("skills"):
            for sk in re.split(r"[,;|]+", a["skills"]):
                sk = sk.strip().title()
                if sk: skills_all.append(sk)
        if a.get("graduation_year"):
            years.append(str(a["graduation_year"]))

    def top(lst, n=8):
        return [{"label": k, "count": v} for k, v in Counter(lst).most_common(n)]

    year_counts = Counter(years)
    trend = [{"year": y, "count": c} for y, c in sorted(year_counts.items())]

    return {
        "top_companies":   top(companies),
        "top_roles":       top(roles),
        "top_skills":      top(skills_all, 12),
        "by_year":         top(years, 10),
        "placement_trend": trend,
        "total_alumni":    len(alumni_data),
        "hiring_domains":  _extract_domains(alumni_data),
    }


def _extract_domains(alumni_data):
    domains = []
    for a in alumni_data:
        role = (a.get("job_role") or "").lower()
        if any(k in role for k in ["software", "developer", "engineer"]): domains.append("Software Engineering")
        elif any(k in role for k in ["data", "analyst", "scientist"]):    domains.append("Data & Analytics")
        elif any(k in role for k in ["product", "manager", "pm"]):        domains.append("Product Management")
        elif any(k in role for k in ["design", "ux", "ui"]):             domains.append("Design")
        elif any(k in role for k in ["finance", "investment", "banking"]): domains.append("Finance")
        else:                                                              domains.append("Other")
    return [{"label": k, "count": v} for k, v in Counter(domains).most_common(8)]


def get_skill_gap(student, target_role, alumni_list):
    target   = target_role.lower()
    relevant = [a for a in alumni_list if target in (a.get("job_role") or "").lower()]
    if not relevant:
        return {"required_skills": [], "student_has": [], "missing": [], "coverage_pct": 0, "role_count": 0, "learning_paths": {}}
    role_skills = Counter()
    for a in relevant:
        for sk in _tokenize_skills(a.get("skills", "")):
            role_skills[sk] += 1
    threshold = max(1, len(relevant) * 0.3)
    required  = {sk for sk, cnt in role_skills.items() if cnt >= threshold}
    s_skills  = _tokenize_skills(student.get("skills", "")) | _tokenize_skills(student.get("interests", ""))
    has     = sorted(required & s_skills)
    missing = sorted(required - s_skills)
    pct     = int(len(has) / len(required) * 100) if required else 100
    return {
        "required_skills": sorted(required),
        "student_has":     has,
        "missing":         missing,
        "coverage_pct":    pct,
        "role_count":      len(relevant),
        "learning_paths":  _suggest_learning_paths(missing),
    }


def _suggest_learning_paths(missing_skills):
    resource_map = {
        "python": "https://docs.python.org/3/tutorial/",
        "sql": "https://www.w3schools.com/sql/",
        "machine learning": "https://www.coursera.org/learn/machine-learning",
        "react": "https://react.dev/learn",
        "docker": "https://docs.docker.com/get-started/",
        "aws": "https://aws.amazon.com/training/",
        "git": "https://git-scm.com/doc",
        "javascript": "https://javascript.info/",
        "kubernetes": "https://kubernetes.io/docs/tutorials/",
        "tensorflow": "https://www.tensorflow.org/tutorials",
        "pytorch": "https://pytorch.org/tutorials/",
    }
    paths = {}
    for skill in missing_skills:
        for key, url in resource_map.items():
            if key in skill.lower():
                paths[skill] = url
                break
    return paths


def compute_placement_score(student, alumni_list):
    if not alumni_list or not student.get("skills"):
        return 0
    top_roles = [a.get("job_role", "") for a in alumni_list if a.get("job_role")]
    if not top_roles:
        return 0
    most_common_role = Counter(top_roles).most_common(1)[0][0]
    gap = get_skill_gap(student, most_common_role, alumni_list)
    return gap.get("coverage_pct", 0)
