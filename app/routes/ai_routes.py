"""app/routes/ai_routes.py — AI Features Hub V5 (CareerGPT, Resume Analyzer, Job Match, Interview Coach)"""
from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, flash
from app.utils.decorators import login_required
from app.models import db, Student, Alumni, Job
import os, json, re

ai_bp = Blueprint("ai", __name__)


def _get_anthropic_client():
    try:
        import anthropic
        key = os.getenv("ANTHROPIC_API_KEY", "")
        if not key:
            return None
        return anthropic.Anthropic(api_key=key)
    except ImportError:
        return None


def _ai_respond(system_prompt, user_message, max_tokens=1000):
    client = _get_anthropic_client()
    if not client:
        return "AI features require ANTHROPIC_API_KEY to be configured. Please add it to your .env file."
    try:
        msg = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return msg.content[0].text
    except Exception as e:
        return f"AI service temporarily unavailable: {str(e)[:100]}"


# ── CareerGPT ──────────────────────────────────────────────────────────────────
@ai_bp.route("/careergpt")
@login_required
def careergpt():
    return render_template("ai/careergpt.html")


@ai_bp.route("/careergpt/chat", methods=["POST"])
@login_required
def careergpt_chat():
    message  = request.json.get("message", "").strip()[:1000]
    history  = request.json.get("history", [])[-10:]  # last 10 turns
    if not message:
        return jsonify({"error": "Empty message"}), 400

    # Build context from user profile
    context = ""
    if session.get("role") == "student":
        student = Student.query.filter_by(user_id=session["user_id"]).first()
        if student:
            context = f"""
User Profile: {session.get('name')} | Student | {student.department} | Year {student.year}
Skills: {student.skills or 'Not specified'}
Interests: {student.interests or 'Not specified'}
"""

    system = f"""You are CareerGPT — an expert AI career assistant for AI CareerVerse platform.
You help students with career advice, resume reviews, job guidance, interview preparation, skill development, and mentor recommendations.
Be encouraging, specific, and practical. Keep responses concise but impactful.
{context}
Platform context: This is an AI-powered career platform connecting students with alumni, mentors, and recruiters in India's tech ecosystem."""

    # Build messages array with history
    messages = []
    for h in history:
        if h.get("role") in ("user", "assistant"):
            messages.append({"role": h["role"], "content": str(h["content"])[:500]})
    messages.append({"role": "user", "content": message})

    client = _get_anthropic_client()
    if not client:
        reply = "CareerGPT requires ANTHROPIC_API_KEY. Please configure it in your .env file to enable AI features."
    else:
        try:
            resp = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=800,
                system=system,
                messages=messages
            )
            reply = resp.content[0].text
        except Exception as e:
            reply = f"AI service temporarily unavailable. Please try again. ({str(e)[:80]})"

    return jsonify({"reply": reply})


# ── Resume Analyzer ────────────────────────────────────────────────────────────
@ai_bp.route("/resume-analyzer")
@login_required
def resume_analyzer():
    return render_template("ai/resume_analyzer.html")


@ai_bp.route("/resume-analyzer/analyze", methods=["POST"])
@login_required
def analyze_resume():
    resume_text = request.form.get("resume_text", "").strip()[:5000]
    target_role = request.form.get("target_role", "Software Engineer").strip()[:100]

    if not resume_text:
        return jsonify({"error": "Resume text is required"}), 400

    system = """You are an expert ATS Resume Analyzer. Analyze resumes and provide structured JSON feedback.
Always respond with valid JSON only, no markdown, no extra text."""

    prompt = f"""Analyze this resume for a {target_role} position.

RESUME:
{resume_text}

Respond with this exact JSON structure:
{{
  "ats_score": 0-100,
  "overall_rating": "Poor/Fair/Good/Excellent",
  "summary": "2-3 sentence overall assessment",
  "strengths": ["strength1", "strength2", "strength3"],
  "improvements": ["improvement1", "improvement2", "improvement3"],
  "missing_keywords": ["keyword1", "keyword2", "keyword3"],
  "formatting_issues": ["issue1"],
  "impact_score": 0-100,
  "keyword_score": 0-100,
  "structure_score": 0-100,
  "recommendations": ["specific recommendation 1", "specific recommendation 2"]
}}"""

    result_text = _ai_respond(system, prompt, max_tokens=1000)
    try:
        clean = re.sub(r"```json|```", "", result_text).strip()
        result = json.loads(clean)
    except Exception:
        result = {
            "ats_score": 65,
            "overall_rating": "Good",
            "summary": result_text[:300],
            "strengths": ["Has relevant experience", "Good structure"],
            "improvements": ["Add more quantifiable achievements", "Include keywords"],
            "missing_keywords": [],
            "formatting_issues": [],
            "impact_score": 65,
            "keyword_score": 60,
            "structure_score": 70,
            "recommendations": ["Tailor your resume to each job description"]
        }
    return jsonify(result)


# ── Resume Builder ─────────────────────────────────────────────────────────────
@ai_bp.route("/resume-builder")
@login_required
def resume_builder():
    student = None
    if session.get("role") == "student":
        student = Student.query.filter_by(user_id=session["user_id"]).first()
    return render_template("ai/resume_builder.html", student=student)


@ai_bp.route("/resume-builder/generate", methods=["POST"])
@login_required
def generate_resume():
    data = request.json or {}
    name       = data.get("name", session.get("name", ""))[:100]
    email      = data.get("email", "")[:150]
    phone      = data.get("phone", "")[:20]
    skills     = data.get("skills", "")[:500]
    experience = data.get("experience", "")[:2000]
    education  = data.get("education", "")[:500]
    projects   = data.get("projects", "")[:1000]
    target_role = data.get("target_role", "Software Engineer")[:100]

    system = "You are a professional resume writer. Generate polished, ATS-optimized resume content."
    prompt = f"""Create a professional resume for:
Name: {name}
Email: {email}
Phone: {phone}
Target Role: {target_role}
Skills: {skills}
Experience: {experience}
Education: {education}
Projects: {projects}

Generate a complete, formatted resume with proper sections. Make it ATS-friendly and impactful.
Use action verbs. Include quantifiable achievements where possible."""

    result = _ai_respond(system, prompt, max_tokens=1500)
    return jsonify({"resume": result})


# ── Job Match Engine ───────────────────────────────────────────────────────────
@ai_bp.route("/job-match")
@login_required
def job_match():
    student = None
    jobs    = Job.query.filter_by(is_active=True).limit(20).all()
    if session.get("role") == "student":
        student = Student.query.filter_by(user_id=session["user_id"]).first()
    return render_template("ai/job_match.html", student=student, jobs=jobs)


@ai_bp.route("/job-match/analyze", methods=["POST"])
@login_required
def analyze_job_match():
    student_skills = request.json.get("student_skills", "")[:500]
    job_id         = request.json.get("job_id")

    job = Job.query.get(job_id) if job_id else None
    if not job:
        return jsonify({"error": "Job not found"}), 404

    system = "You are an AI job matching expert. Analyze skill fit and provide JSON responses only."
    prompt = f"""Match this candidate to the job:

CANDIDATE SKILLS: {student_skills}

JOB: {job.title} at {job.company}
REQUIRED SKILLS: {job.skills_required or 'Not specified'}
DESCRIPTION: {(job.description or '')[:500]}

Respond with JSON only:
{{
  "match_score": 0-100,
  "match_level": "Poor/Fair/Good/Strong",
  "matched_skills": ["skill1"],
  "missing_skills": ["skill1"],
  "strengths": ["point1"],
  "gaps": ["gap1"],
  "recommendation": "Should you apply? Why?",
  "preparation_tips": ["tip1", "tip2"]
}}"""

    result_text = _ai_respond(system, prompt, max_tokens=800)
    try:
        clean = re.sub(r"```json|```", "", result_text).strip()
        result = json.loads(clean)
    except Exception:
        result = {
            "match_score": 70,
            "match_level": "Good",
            "matched_skills": [],
            "missing_skills": [],
            "strengths": ["Relevant background"],
            "gaps": [],
            "recommendation": result_text[:300],
            "preparation_tips": []
        }
    result["job_title"]   = job.title
    result["job_company"] = job.company
    return jsonify(result)


# ── Skill Gap Analyzer ─────────────────────────────────────────────────────────
@ai_bp.route("/skill-gap")
@login_required
def ai_skill_gap():
    return render_template("ai/skill_gap.html")


@ai_bp.route("/skill-gap/analyze", methods=["POST"])
@login_required
def analyze_skill_gap():
    current_skills = request.json.get("current_skills", "")[:500]
    dream_role     = request.json.get("dream_role", "")[:100]

    if not dream_role:
        return jsonify({"error": "Dream role is required"}), 400

    system = "You are a career development expert. Provide skill gap analysis in JSON only."
    prompt = f"""Skill gap analysis:
CURRENT SKILLS: {current_skills or 'None specified'}
DREAM ROLE: {dream_role}

Respond with JSON:
{{
  "role_overview": "Brief description of {dream_role}",
  "required_skills": ["skill1", "skill2"],
  "skills_you_have": ["skill1"],
  "missing_skills": ["skill1"],
  "priority_skills": ["most important missing skills"],
  "learning_paths": {{
    "skill_name": {{"resource": "URL or platform", "time": "estimated weeks", "difficulty": "Beginner/Intermediate/Advanced"}}
  }},
  "roadmap": {{
    "0_3_months": ["action1"],
    "3_6_months": ["action2"],
    "6_12_months": ["action3"]
  }},
  "readiness_score": 0-100
}}"""

    result_text = _ai_respond(system, prompt, max_tokens=1200)
    try:
        clean = re.sub(r"```json|```", "", result_text).strip()
        result = json.loads(clean)
    except Exception:
        result = {
            "role_overview": f"Overview of {dream_role}",
            "required_skills": ["Python", "SQL", "Communication"],
            "skills_you_have": [],
            "missing_skills": [],
            "priority_skills": [],
            "learning_paths": {},
            "roadmap": {"0_3_months": [], "3_6_months": [], "6_12_months": []},
            "readiness_score": 50
        }
    return jsonify(result)


# ── Career Roadmap ─────────────────────────────────────────────────────────────
@ai_bp.route("/career-roadmap")
@login_required
def career_roadmap():
    return render_template("ai/career_roadmap.html")


@ai_bp.route("/career-roadmap/generate", methods=["POST"])
@login_required
def generate_roadmap():
    current_role = request.json.get("current_role", "Student")[:100]
    target_role  = request.json.get("target_role", "")[:100]
    skills       = request.json.get("skills", "")[:500]
    timeline     = request.json.get("timeline", "12 months")[:30]

    system = "You are a career coach creating personalized roadmaps. Respond in JSON only."
    prompt = f"""Create a career roadmap:
FROM: {current_role}
TO: {target_role}
CURRENT SKILLS: {skills}
TIMELINE: {timeline}

JSON response:
{{
  "title": "Your Roadmap to {target_role}",
  "overview": "Brief personalized overview",
  "phases": [
    {{
      "phase": "Phase 1",
      "duration": "0-3 months",
      "focus": "Foundation",
      "goals": ["goal1"],
      "skills_to_learn": ["skill1"],
      "projects": ["project1"],
      "certifications": ["cert1"],
      "milestones": ["milestone1"]
    }}
  ],
  "daily_habits": ["habit1"],
  "weekly_goals": ["goal1"],
  "resources": [
    {{"name": "resource", "url": "link", "type": "course/book/community"}}
  ],
  "success_metrics": ["metric1"]
}}"""

    result_text = _ai_respond(system, prompt, max_tokens=1500)
    try:
        clean = re.sub(r"```json|```", "", result_text).strip()
        result = json.loads(clean)
    except Exception:
        result = {
            "title": f"Roadmap to {target_role}",
            "overview": result_text[:500],
            "phases": [],
            "daily_habits": [],
            "weekly_goals": [],
            "resources": [],
            "success_metrics": []
        }
    return jsonify(result)


# ── Interview Coach ────────────────────────────────────────────────────────────
@ai_bp.route("/interview-coach")
@login_required
def interview_coach():
    return render_template("ai/interview_coach.html")


@ai_bp.route("/interview-coach/question", methods=["POST"])
@login_required
def get_interview_question():
    interview_type = request.json.get("type", "hr")[:20]
    role           = request.json.get("role", "Software Engineer")[:100]
    difficulty     = request.json.get("difficulty", "medium")[:20]

    system = "You are an expert interviewer. Generate realistic interview questions with context."
    prompt = f"""Generate ONE {interview_type} interview question for a {role} position ({difficulty} level).

Respond in JSON:
{{
  "question": "The interview question",
  "type": "{interview_type}",
  "hints": ["hint1", "hint2"],
  "what_interviewer_wants": "What they're looking for",
  "example_answer_structure": "How to structure the answer"
}}"""

    result_text = _ai_respond(system, prompt, max_tokens=600)
    try:
        clean = re.sub(r"```json|```", "", result_text).strip()
        result = json.loads(clean)
    except Exception:
        result = {
            "question": result_text[:300],
            "type": interview_type,
            "hints": [],
            "what_interviewer_wants": "",
            "example_answer_structure": ""
        }
    return jsonify(result)


@ai_bp.route("/interview-coach/evaluate", methods=["POST"])
@login_required
def evaluate_answer():
    question = request.json.get("question", "")[:500]
    answer   = request.json.get("answer", "")[:2000]
    role     = request.json.get("role", "Software Engineer")[:100]

    if not question or not answer:
        return jsonify({"error": "Question and answer required"}), 400

    system = "You are a senior technical interviewer. Evaluate answers and give constructive feedback in JSON."
    prompt = f"""Evaluate this interview answer for {role}:

QUESTION: {question}
ANSWER: {answer}

Respond in JSON:
{{
  "score": 0-100,
  "rating": "Poor/Fair/Good/Excellent",
  "strengths": ["strength1"],
  "improvements": ["improvement1"],
  "ideal_answer_elements": ["element1"],
  "follow_up_questions": ["question1"],
  "feedback": "Detailed constructive feedback (3-4 sentences)",
  "star_method_used": true/false,
  "confidence_tips": ["tip1"]
}}"""

    result_text = _ai_respond(system, prompt, max_tokens=800)
    try:
        clean = re.sub(r"```json|```", "", result_text).strip()
        result = json.loads(clean)
    except Exception:
        result = {
            "score": 70,
            "rating": "Good",
            "strengths": [],
            "improvements": [],
            "ideal_answer_elements": [],
            "follow_up_questions": [],
            "feedback": result_text[:400],
            "star_method_used": False,
            "confidence_tips": []
        }
    return jsonify(result)
