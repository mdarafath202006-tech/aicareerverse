# 🚀 AI CareerVerse V5

> The AI-powered career ecosystem connecting students with alumni, mentors, and opportunities.

---

## 📋 Table of Contents
1. [What's New in V5](#whats-new-in-v5)
2. [Architecture Overview](#architecture-overview)
3. [Quick Start (Local)](#quick-start-local)
4. [Deploy to Render (Production)](#deploy-to-render)
5. [Environment Variables](#environment-variables)
6. [Database & Seed Data](#database--seed-data)
7. [User Roles & Demo Credentials](#user-roles--demo-credentials)
8. [Feature Guide](#feature-guide)
9. [AI Features Setup](#ai-features-setup)
10. [Project Structure](#project-structure)

---

## What's New in V5

| Feature | V3 | V5 |
|---------|----|----|
| Referral System | ❌ | ✅ Full workflow: request → approve/reject → notify |
| Company Pages | ❌ | ✅ 8 companies with jobs + alumni directory |
| Knowledge Base | ❌ | ✅ Alumni stories, interview experiences, career guides |
| CareerGPT | Basic | ✅ Full multi-turn chat with profile context |
| Resume Analyzer | ❌ | ✅ ATS score, keyword gaps, structured feedback |
| Resume Builder | ❌ | ✅ AI-generated ATS-optimized resumes |
| Job Match Engine | ❌ | ✅ Per-job match score + preparation tips |
| Skill Gap Analyzer | Basic | ✅ Learning paths, roadmap, priority skills |
| Career Roadmap | ❌ | ✅ Phase-by-phase with projects & certifications |
| Interview Coach | ❌ | ✅ Question generation + answer scoring |
| Follow System | ❌ | ✅ Follow alumni, get activity in feed |
| Alumni Profile Page | ❌ | ✅ Public profile with CTA buttons |
| Admin Dashboard | Basic | ✅ Full stats, user management, analytics |
| Seed Data | Minimal | ✅ 32 users, 8 companies, 22 jobs, 100+ posts, 5 knowledge entries |

---

## Architecture Overview

```
aicareerverse_v5/
├── app/
│   ├── __init__.py           # Application factory, SocketIO, CSRF, rate limiting
│   ├── models/               # SQLAlchemy ORM models
│   │   ├── user.py           # User (all roles) + profile_completion()
│   │   ├── student.py        # Student profile
│   │   ├── alumni.py         # Alumni profile
│   │   ├── mentorship.py     # Mentorship requests & sessions
│   │   ├── post.py           # Posts, comments, likes
│   │   ├── job.py            # Job listings & applications
│   │   ├── community.py      # Communities & memberships
│   │   ├── referral.py       # NEW: Referral system
│   │   ├── company.py        # NEW: Company pages
│   │   ├── knowledge.py      # NEW: Knowledge base entries
│   │   ├── follow.py         # NEW: Follow/unfollow users
│   │   ├── notification.py   # Real-time notifications
│   │   ├── gamification.py   # Points & badges
│   │   └── project.py        # Project showcases
│   ├── routes/
│   │   ├── student.py        # Student dashboard, profile, search, mentorship
│   │   ├── alumni.py         # Alumni dashboard, profile, mentorship responses
│   │   ├── feed.py           # Social feed, posts, likes, comments
│   │   ├── jobs.py           # Job listings & applications
│   │   ├── communities.py    # Communities
│   │   ├── referrals.py      # NEW: Full referral workflow
│   │   ├── companies.py      # NEW: Company pages
│   │   ├── knowledge.py      # NEW: Knowledge base CRUD
│   │   ├── ai_routes.py      # NEW: All 7 AI features
│   │   ├── analytics.py      # Analytics dashboard
│   │   └── admin.py          # Admin panel
│   ├── ai/
│   │   └── recommender.py    # Skill-based alumni recommender
│   ├── api/routes.py         # JSON REST API endpoints
│   ├── auth/routes.py        # Login, register, logout
│   ├── repositories/         # Data access layer
│   ├── utils/decorators.py   # login_required, role_required
│   └── templates/            # Jinja2 HTML templates
├── migrations/
│   └── seed_v5.py            # Full demo data seeder
├── config.py                 # Dev / Prod / Test configs
├── run.py                    # Entry point
├── requirements.txt
├── Procfile                  # For Render/Heroku
├── render.yaml               # One-click Render deployment
└── .env.example              # All required environment variables
```

**Tech Stack:** Python · Flask · SQLAlchemy · PostgreSQL · Redis · Flask-SocketIO · Gunicorn · Anthropic Claude API

---

## Quick Start (Local)

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis (optional — used for rate limiting & caching)

### Step-by-step

```bash
# 1. Clone / extract the project
cd aicareerverse_v5

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env — minimum required:
#   DATABASE_URL=postgresql://postgres:password@localhost:5432/aicareerverse
#   SECRET_KEY=any-long-random-string
#   ANTHROPIC_API_KEY=sk-ant-...    ← get from console.anthropic.com (free trial available)

# 5. Create the database
createdb aicareerverse             # or use pgAdmin / psql

# 6. Run migrations
flask db upgrade

# 7. Seed demo data
python migrations/seed_v5.py

# 8. Start the server
python run.py
# → http://localhost:5000
```

### Start with development config (hot reload):
```bash
FLASK_ENV=development python run.py
```

---

## Deploy to Render

### Option A — render.yaml (one-click, recommended)

1. Push code to a GitHub repository
2. Go to [render.com](https://render.com) → New → Blueprint
3. Connect your repo → Render reads `render.yaml` and provisions everything automatically
4. Add your `ANTHROPIC_API_KEY` in Render → Environment → Add Secret

### Option B — Manual

1. Create a **PostgreSQL** database on Render (free tier)
2. Create a **Redis** instance on Render (free tier)
3. Create a **Web Service**:
   - **Build command:** `pip install -r requirements.txt && flask db upgrade && python migrations/seed_v5.py`
   - **Start command:** `gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:$PORT --timeout 120 run:app`
4. Set environment variables (see below)

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | ✅ | Flask session secret — use 32+ random chars |
| `JWT_SECRET_KEY` | ✅ | JWT signing key |
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `ANTHROPIC_API_KEY` | ✅ for AI | Get from [console.anthropic.com](https://console.anthropic.com) |
| `REDIS_URL` | Recommended | Rate limiting & caching. Falls back to in-memory |
| `CLOUDINARY_CLOUD_NAME` | Optional | For image uploads |
| `CLOUDINARY_API_KEY` | Optional | For image uploads |
| `CLOUDINARY_API_SECRET` | Optional | For image uploads |
| `FLASK_ENV` | Optional | `development` or `production` (default) |

---

## Database & Seed Data

### Run migrations
```bash
flask db upgrade
```

### Seed demo data
```bash
python migrations/seed_v5.py
```

This creates:

| Category | Count |
|----------|-------|
| Admin users | 1 |
| Students | 15 |
| Alumni (with mentorship/referral capability) | 8 |
| Companies | 8 |
| Jobs (mix of internships + full-time) | 22 |
| Communities | 5 |
| Posts | ~100 |
| Mentorship requests | ~25 |
| Referral records | ~10 |
| Job applications | ~60 |
| Knowledge base entries | 5 |
| Follow relationships | ~30 |

### Reset & re-seed
```bash
# Drop and recreate
dropdb aicareerverse && createdb aicareerverse
flask db upgrade
python migrations/seed_v5.py
```

---

## User Roles & Demo Credentials

| Role | Email | Password | What they can do |
|------|-------|----------|-----------------|
| **Admin** | `admin@demo.com` | `Demo@1234` | Manage users, view all analytics, moderate content |
| **Student** | `student@demo.com` | `Demo@1234` | Browse jobs, request mentors, request referrals, use AI tools |
| **Alumni** | `alumni@demo.com` | `Demo@1234` | Manage mentorship requests, approve/reject referrals, post jobs |

> All 32 seeded users share password `Demo@1234`

---

## Feature Guide

### Social Feed (`/student/feed` · `/alumni/feed`)
- Create posts (text, achievement, opportunity announcements)
- Like, comment, share posts
- Trending feed sorted by engagement + recency

### Job Portal (`/jobs`)
- Browse 22 demo jobs with filters (type, keyword)
- Apply with cover letter
- Alumni can post new jobs

### Mentorship System
- **Student:** Browse AI-recommended alumni → Send request with personal message
- **Alumni:** Dashboard shows pending requests → Accept or decline
- Real-time notification via SocketIO on accept/decline

### Referral System (`/referrals/`)
- **Student:** Visit alumni profile → "Request Referral" → Fill company/position/message
- **Alumni:** Referral requests dashboard → Approve with note or decline
- Status tracked: pending → approved/rejected
- Both parties notified in real-time

### Company Pages (`/companies/`)
- Browse 8 companies with descriptions, industry, size
- Each company page shows: open jobs, alumni working there, hiring status

### Knowledge Base (`/knowledge/`)
- 6 categories: Success Stories, Interview Experiences, Placement Stories, Career Guides, Company Reviews, Tips & Tricks
- Search by keyword, company, role
- Alumni share multi-paragraph stories
- Helpful count + view count tracking

### AI Tools Hub (`/ai-tools`)

| Tool | Route | Description |
|------|-------|-------------|
| **CareerGPT** | `/ai/careergpt` | Multi-turn AI career chat assistant with quick prompts |
| **Resume Analyzer** | `/ai/resume-analyzer` | ATS score (0-100), keywords, structure, impact scores |
| **Resume Builder** | `/ai/resume-builder` | Fill form → AI generates complete formatted resume |
| **Job Match Engine** | `/ai/job-match` | Select job → AI scores your match + preparation tips |
| **Skill Gap Analyzer** | `/ai/skill-gap` | Enter dream role → missing skills + learning paths |
| **Career Roadmap** | `/ai/career-roadmap` | Phase-by-phase roadmap with projects & certifications |
| **Interview Coach** | `/ai/interview-coach` | Practice questions + AI scores your answers 0-100 |

> All AI tools require `ANTHROPIC_API_KEY`. Without it they return a helpful configuration message.

---

## AI Features Setup

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Create account → API Keys → Create Key
3. New accounts receive $5 free credit (enough for thousands of AI interactions)
4. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-your-key`

All AI features use `claude-3-haiku-20240307` — the fastest, most cost-efficient model in the Claude 3 family. A typical student session (10 AI interactions) costs less than $0.01.

---

## Project Structure (Key Files)

```
app/routes/ai_routes.py     ← All 7 AI features (CareerGPT, analyzer, builder, match, gap, roadmap, interview)
app/routes/referrals.py     ← Referral request, respond workflow
app/routes/companies.py     ← Company pages
app/routes/knowledge.py     ← Knowledge base CRUD
app/models/referral.py      ← Referral DB model
app/models/company.py       ← Company DB model
app/models/knowledge.py     ← Knowledge entry DB model
app/models/follow.py        ← Follow relationship model
migrations/seed_v5.py       ← Full demo data (32 users, 22 jobs, 100+ posts)
```

---

## Common Issues

**`CSRF token missing`** — Make sure `{{ csrf_token() }}` is in every POST form. The V5 app factory enables WTF CSRF globally.

**`eventlet` import error** — Run `pip install eventlet==0.36.1`. Required for Flask-SocketIO.

**`psycopg2` error on Apple Silicon** — Use `pip install psycopg2-binary` (not `psycopg2`).

**AI features return "API key not configured"** — Add `ANTHROPIC_API_KEY` to your `.env` file.

**Redis connection refused** — Set `REDIS_URL=memory://` in `.env` for local dev without Redis.

---

## License

MIT — built for educational and portfolio purposes.
