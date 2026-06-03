#!/usr/bin/env python3
"""
AI CareerVerse V3 — Complete Demo Seed Script
Creates realistic demo ecosystem with 10 students, 10 alumni, posts,
communities, jobs, mentorships, notifications, and gamification data.

Run: python migrations/seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models.base import db
from app.models import (
    User, Student, Alumni, MentorshipRequest,
    Post, Comment, Like, Notification,
    Community, CommunityMember,
    Job, JobApplication,
    ProjectShowcase, UserPoints, UserBadge,
)
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

app = create_app("config.DevelopmentConfig")

DEMO_PASSWORD = generate_password_hash("Demo@1234")

# ─── STUDENTS ─────────────────────────────────────────────────────────────────
STUDENTS = [
    dict(name="Arjun Verma",     email="student@demo.com",          department="Computer Science",   year="3rd",
         skills="Python,React,Machine Learning,SQL",    interests="AI/ML,Product Management",
         bio="Passionate about AI and building impactful products. Always eager to connect with amazing people.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Priya Kapoor",    email="priya.kapoor@demo.com",     department="Data Science",        year="4th",
         skills="Python,TensorFlow,Statistics,Tableau", interests="Data Science,Finance,ML",
         bio="Data Science student with a passion for turning data into meaningful insights.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Neha Sharma",     email="neha.sharma@demo.com",      department="Cybersecurity",       year="2nd",
         skills="Network Security,Linux,Python,OWASP",  interests="Cybersecurity,Ethical Hacking",
         bio="Cybersecurity enthusiast committed to building safer digital systems.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Rohan Mehta",     email="rohan.mehta@demo.com",      department="Computer Science",   year="3rd",
         skills="JavaScript,React,Node.js,MongoDB",     interests="Full Stack,Startups",
         bio="Full stack developer who loves building user-friendly web applications.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Ananya Singh",    email="ananya.singh@demo.com",      department="AI & ML",            year="4th",
         skills="PyTorch,NLP,Python,Transformers",      interests="Natural Language Processing,Research",
         bio="NLP researcher working on multilingual language models for low-resource languages.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Vikram Rao",      email="vikram.rao@demo.com",        department="Electronics",         year="2nd",
         skills="C++,Embedded Systems,Arduino,IoT",     interests="IoT,Robotics,Hardware",
         bio="Hardware enthusiast building IoT solutions for smart agriculture.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Kavya Reddy",     email="kavya.reddy@demo.com",       department="Computer Science",   year="1st",
         skills="Python,HTML,CSS,Java",                  interests="UI/UX,Mobile Development",
         bio="First year CS student eager to learn and build cool things.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Aditya Kumar",    email="aditya.kumar@demo.com",      department="Information Tech",   year="3rd",
         skills="DevOps,Docker,Kubernetes,AWS",          interests="Cloud,DevOps,SRE",
         bio="DevOps enthusiast automating everything I can find.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Pooja Iyer",      email="pooja.iyer@demo.com",        department="Data Science",        year="2nd",
         skills="R,Python,Statistics,Power BI",          interests="Business Analytics,Finance",
         bio="Aspiring data analyst who loves uncovering stories hidden in numbers.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
    dict(name="Siddharth Nair",  email="siddharth.nair@demo.com",    department="Computer Science",   year="4th",
         skills="System Design,Java,Spring Boot,SQL",    interests="Backend,Distributed Systems",
         bio="Backend engineer at heart. Building scalable systems is my passion.",
         github_url="https://github.com", linkedin_url="https://linkedin.com"),
]

# ─── ALUMNI ───────────────────────────────────────────────────────────────────
ALUMNI = [
    dict(name="Priya Sharma",    email="alumni@demo.com",            company="Google",    job_role="Senior Product Manager",
         graduation_year=2020, location="Bangalore, India",
         skills="Product Management,Strategy,Analytics,Leadership",
         bio="Passionate about building products that create impact. Happy to mentor and guide students.",
         domain="Product Management", mentorship_slots=5, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=92, mentorship_score=88),
    dict(name="Rahul Gupta",     email="rahul.gupta@demo.com",       company="Microsoft", job_role="Software Engineer L5",
         graduation_year=2019, location="Hyderabad, India",
         skills="C#,.NET,Azure,System Design,Distributed Systems",
         bio="Building cloud-scale systems at Microsoft. Love helping aspiring engineers.",
         domain="Backend Engineering", mentorship_slots=4, is_hiring=False,
         linkedin="https://linkedin.com", impact_score=85, mentorship_score=80),
    dict(name="Kavya Pillai",    email="kavya.pillai@demo.com",      company="Amazon",    job_role="Machine Learning Engineer",
         graduation_year=2021, location="Chennai, India",
         skills="TensorFlow,PyTorch,Python,MLOps,AWS SageMaker",
         bio="ML engineer at Amazon Alexa. Passionate about NLP and conversational AI.",
         domain="Machine Learning", mentorship_slots=3, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=78, mentorship_score=75),
    dict(name="Arjun Patel",     email="arjun.patel@demo.com",       company="Flipkart",  job_role="Senior SDE",
         graduation_year=2018, location="Bangalore, India",
         skills="Java,Microservices,Kafka,Redis,System Design",
         bio="7 years building e-commerce infrastructure at scale. Happy to share learnings.",
         domain="Backend Engineering", mentorship_slots=3, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=88, mentorship_score=82),
    dict(name="Meera Krishnan",  email="meera.krishnan@demo.com",    company="Razorpay",  job_role="Engineering Manager",
         graduation_year=2017, location="Bangalore, India",
         skills="Engineering Management,Go,System Design,Leadership,FinTech",
         bio="Building India's payment infrastructure. Passionate about developer experience and team building.",
         domain="Engineering Leadership", mentorship_slots=2, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=95, mentorship_score=90),
    dict(name="Kiran Reddy",     email="kiran.reddy@demo.com",       company="Swiggy",    job_role="Data Scientist",
         graduation_year=2020, location="Hyderabad, India",
         skills="Python,PySpark,Airflow,ML,SQL,Tableau",
         bio="Using data to optimize food delivery at massive scale. Let's talk data science!",
         domain="Data Science", mentorship_slots=4, is_hiring=False,
         linkedin="https://linkedin.com", impact_score=72, mentorship_score=68),
    dict(name="Ankit Shah",      email="ankit.shah@demo.com",        company="Zepto",     job_role="Co-Founder & CTO",
         graduation_year=2019, location="Mumbai, India",
         skills="Startups,Engineering,Leadership,Fundraising,Product",
         bio="Building quick-commerce infrastructure from scratch. Happy to share my startup journey.",
         domain="Startups", mentorship_slots=2, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=98, mentorship_score=95),
    dict(name="Sneha Agarwal",   email="sneha.agarwal@demo.com",     company="Infosys",   job_role="Cybersecurity Lead",
         graduation_year=2016, location="Pune, India",
         skills="Penetration Testing,SIEM,Incident Response,CISSP,Python",
         bio="10 years in cybersecurity. Helping the next generation secure the digital world.",
         domain="Cybersecurity", mentorship_slots=5, is_hiring=False,
         linkedin="https://linkedin.com", impact_score=82, mentorship_score=78),
    dict(name="Rohan Joshi",     email="rohan.joshi@demo.com",       company="Adobe",     job_role="Staff Frontend Engineer",
         graduation_year=2018, location="Noida, India",
         skills="React,TypeScript,GraphQL,Performance,Design Systems",
         bio="Building creative tools for millions of designers. Passionate about great UX.",
         domain="Frontend Engineering", mentorship_slots=4, is_hiring=False,
         linkedin="https://linkedin.com", impact_score=80, mentorship_score=76),
    dict(name="Divya Menon",     email="divya.menon@demo.com",       company="Atlassian", job_role="DevOps Engineer",
         graduation_year=2021, location="Remote",
         skills="Kubernetes,Terraform,CI/CD,AWS,Observability",
         bio="Platform engineer at Atlassian. Helping teams ship faster with better infrastructure.",
         domain="DevOps & Cloud", mentorship_slots=3, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=74, mentorship_score=70),
]

# ─── COMMUNITIES ──────────────────────────────────────────────────────────────
COMMUNITIES = [
    dict(name="AI & Machine Learning", slug="ai-ml",   icon="🤖", description="Deep learning, NLP, computer vision, and everything AI. For researchers and practitioners alike.", member_count=2400, post_count=340),
    dict(name="Web Development",       slug="webdev",  icon="🌐", description="Frontend, backend, full-stack. From React to Django, everything web.", member_count=3100, post_count=520),
    dict(name="Cybersecurity",         slug="cybersec",icon="🔒", description="Ethical hacking, blue team, security research, and CTF challenges.", member_count=1800, post_count=210),
    dict(name="Data Science",          slug="datascience",icon="📊",description="Statistics, data engineering, BI, and ML in industry.", member_count=2900, post_count=480),
    dict(name="DevOps & Cloud",        slug="devops",  icon="⚙️", description="CI/CD, containers, Kubernetes, AWS, GCP, Azure. Ship faster.", member_count=1500, post_count=190),
    dict(name="Startups & Product",    slug="startups",icon="🚀", description="Building from zero. Founders, PMs, and growth hackers welcome.", member_count=1200, post_count=270),
    dict(name="Mobile Development",    slug="mobile",  icon="📱", description="iOS, Android, Flutter, React Native. Building the apps people love.", member_count=980,  post_count=145),
    dict(name="Open Source",           slug="opensource",icon="💻",description="Contributing to open source, maintaining projects, and OSS culture.", member_count=720,  post_count=98),
]

# ─── POSTS ────────────────────────────────────────────────────────────────────
POSTS_DATA = [
    dict(type="achievement", content="🎉 So excited to share that I just received my offer letter from Google! This journey wouldn't have been possible without the amazing mentors on this platform. Priya Sharma's guidance was invaluable. If you're preparing for FAANG — believe in yourself and use the resources here! #Google #FAANG #CareerVerse", tags="Google,FAANG,Placement,Gratitude"),
    dict(type="opportunity", content="📢 We're hiring! Zepto is looking for SDE-1 and SDE-2 engineers in Bangalore and Mumbai. 6-15 LPA. Great culture, fast growth, real ownership from day one. DM me or apply through the jobs portal. #Hiring #Zepto #SDE", tags="Hiring,Zepto,Jobs,Engineering"),
    dict(type="text", content="Just completed my first end-to-end ML project — a sentiment analysis model for product reviews with 92% accuracy. Using BERT fine-tuned on a custom dataset. The hardest part? Getting the data pipeline right. If you're starting with NLP, focus on data quality first! 🤖", tags="MachineLearning,NLP,BERT,Python"),
    dict(type="achievement", content="Passed the AWS Solutions Architect Associate exam on my first attempt! ☁️ The resources that helped most: AWS documentation (seriously!), practice exams, and hands-on labs. Took 3 months of part-time prep. Happy to share my study plan — just comment below.", tags="AWS,Cloud,Certification,DevOps"),
    dict(type="text", content="Hot take: System design skills are becoming more important than DSA for senior roles. After interviewing at 5 companies, the pattern is clear — everyone wants you to design distributed systems. Start learning it early, not just for interviews but because it'll make you a better engineer. 🏗️", tags="SystemDesign,SoftwareEngineering,Interviews,Career"),
    dict(type="opportunity", content="Razorpay is hiring SDE-2 backend engineers! We're building India's payments infrastructure and looking for people who love solving complex distributed systems problems. Apply here or connect with me for a referral. The tech stack: Go, gRPC, Kafka, PostgreSQL. #Razorpay #Hiring", tags="Razorpay,Hiring,Backend,FinTech"),
    dict(type="achievement", content="Just presented my research paper on 'Efficient Transformers for Low-Resource Languages' at the ACL workshop! First time presenting at an international NLP conference. The feedback was incredible and I've made connections that'll last a lifetime. Grateful for all the support! 📄", tags="NLP,Research,ACL,TransferLearning"),
    dict(type="text", content="Hackathon season is here! 🚀 For all students: hackathons are the best way to learn fast, build your portfolio, and meet amazing people. I've won 3 hackathons this year and each one taught me more than months of coursework. Check the events section for upcoming ones!", tags="Hackathon,StudentLife,Portfolio,Networking"),
    dict(type="text", content="PSA for job seekers: LinkedIn easy apply alone won't get you hired. The best results come from: 1) Referrals from connections 2) Direct outreach to hiring managers 3) Contributing to company OSS repos. Work smarter, not harder. 💡", tags="JobSearch,Career,Networking,Tips"),
    dict(type="achievement", content="6 months into my journey at Microsoft and I already shipped a feature used by 50M+ users worldwide! Never thought this was possible when I was struggling with DSA problems in college. The learning curve is steep but the growth is real. Keep going! 💪", tags="Microsoft,Career,Growth,SoftwareEngineering"),
    dict(type="text", content="Reading 'Designing Data-Intensive Applications' by Martin Kleppmann. Hands down the best technical book I've read in years. If you're serious about backend or distributed systems, this is mandatory reading. Which books have shaped your engineering thinking?", tags="Books,DistributedSystems,Learning,Engineering"),
    dict(type="opportunity", content="Adobe is looking for Frontend interns for Summer 2025! Location: Noida. Duration: 6 months. Stipend: ₹40k/month. Stack: React, TypeScript, GraphQL. Apply through our jobs portal or DM me. Deadline: January 15. #Adobe #Internship #Frontend", tags="Adobe,Internship,Frontend,React"),
    dict(type="achievement", content="My open source project hit 1000 GitHub stars today! 🌟 It's a React component library for data visualization. Never thought I'd build something people actually use. Open source is the best way to build real credibility. Go check it out! #OpenSource #React", tags="OpenSource,React,GitHub,Milestone"),
    dict(type="text", content="Cybersecurity tip of the week: Always use a password manager. I can't stress this enough. 80% of breaches involve compromised credentials. Use Bitwarden (free and open source) or 1Password. Your future self will thank you. 🔒 #CyberSecurity #Security #Tips", tags="Cybersecurity,Security,Tips,Privacy"),
    dict(type="text", content="For students preparing for placements: the 'Interview Prep' tool in AI Tools section is genuinely useful. It gave me exactly the questions that came up in my Google L4 interview. Use the resources the platform provides — they're here for a reason! ✨", tags="Placement,Interview,Tips,CareerVerse"),
]

# ─── JOBS ────────────────────────────────────────────────────────────────────
JOBS_DATA = [
    dict(title="Software Engineer Intern", company="Google",   location="Bangalore", job_type="internship",
         description="Join Google's engineering team for a 6-month internship. Work on real projects with millions of users.",
         requirements="3rd or 4th year CS students. Strong DSA fundamentals.", skills_required="Python,C++,Algorithms",
         salary_range="₹80k/month"),
    dict(title="SDE-1 Backend Engineer", company="Razorpay", location="Bangalore", job_type="full_time",
         description="Build India's payments infrastructure from the ground up. Own features end-to-end.",
         requirements="0-2 years exp. Strong in distributed systems.", skills_required="Go,PostgreSQL,Kafka,System Design",
         salary_range="₹18-25 LPA"),
    dict(title="ML Engineer", company="Amazon",   location="Hyderabad", job_type="full_time",
         description="Join Alexa ML team to build conversational AI systems used by millions.",
         requirements="1-3 years exp in ML. Strong Python and modeling skills.", skills_required="Python,PyTorch,NLP,AWS SageMaker",
         salary_range="₹30-45 LPA"),
    dict(title="Frontend Engineer Intern", company="Adobe",  location="Noida", job_type="internship",
         description="Build UI components for Creative Cloud products used by 30M+ designers worldwide.",
         requirements="2nd-4th year students. Strong React fundamentals.", skills_required="React,TypeScript,CSS,GraphQL",
         salary_range="₹40k/month"),
    dict(title="DevOps Engineer", company="Atlassian", location="Remote", job_type="full_time",
         description="Build and maintain infrastructure for Jira, Confluence, and Bitbucket.",
         requirements="2+ years DevOps experience. Strong cloud skills.", skills_required="Kubernetes,Terraform,AWS,CI/CD",
         salary_range="₹25-38 LPA"),
    dict(title="Data Scientist", company="Swiggy", location="Bangalore", job_type="full_time",
         description="Use data to optimize food delivery logistics and customer experience at massive scale.",
         requirements="1-3 years ML experience. Strong statistics background.", skills_required="Python,PySpark,SQL,ML",
         salary_range="₹20-30 LPA"),
    dict(title="Product Manager Intern", company="Flipkart", location="Bangalore", job_type="internship",
         description="Define product roadmaps for India's largest e-commerce platform.",
         requirements="MBA or final year students. Analytical mindset.", skills_required="Product Strategy,Analytics,SQL",
         salary_range="₹60k/month"),
    dict(title="Cybersecurity Analyst", company="Infosys", location="Pune", job_type="full_time",
         description="Protect enterprise systems from threats. Run penetration tests and incident response.",
         requirements="CEH or OSCP preferred. 0-2 years experience.", skills_required="Penetration Testing,SIEM,Python,Linux",
         salary_range="₹8-14 LPA"),
]

# ─── PROJECTS ────────────────────────────────────────────────────────────────
PROJECTS_DATA = [
    dict(title="AI Resume Analyzer", description="NLP-based resume analyzer using BERT that extracts skills and suggests improvements. Built for 500+ users.", tech_stack="Python,BERT,FastAPI,React", github_url="https://github.com", demo_url="https://demo.ai", likes_count=142),
    dict(title="HealthTrack IoT", description="Wearable health monitoring system using Arduino + ML anomaly detection. Won 1st place at national hackathon.", tech_stack="C++,Arduino,Python,TensorFlow", github_url="https://github.com", demo_url=None, likes_count=89),
    dict(title="EduConnect Platform", description="Peer tutoring marketplace connecting students for collaborative learning with real-time video sessions.", tech_stack="React,Node.js,WebRTC,MongoDB", github_url="https://github.com", demo_url="https://demo.edu", likes_count=203),
    dict(title="Carbon Footprint Tracker", description="Web app that calculates and tracks your personal carbon footprint with AI-driven reduction recommendations.", tech_stack="Vue.js,Python,Flask,PostgreSQL", github_url="https://github.com", demo_url="https://demo.carbon", likes_count=67),
    dict(title="SecureVault", description="Zero-knowledge encrypted note-taking app. Your data is encrypted client-side — even the server can't read it.", tech_stack="React,Node.js,AES-256,SQLite", github_url="https://github.com", demo_url=None, likes_count=156),
    dict(title="OpenMart", description="Open-source marketplace for local artisans. Supports UPI, multilingual interface in 8 Indian languages.", tech_stack="Next.js,Django,PostgreSQL,Redis", github_url="https://github.com", demo_url="https://openmart.demo", likes_count=318),
]


def seed():
    print("🌱 Seeding AI CareerVerse V3 demo data...")
    with app.app_context():
        db.create_all()

        # ── Admin ──────────────────────────────────────
        if not User.query.filter_by(email="admin@demo.com").first():
            admin = User(name="Admin", email="admin@demo.com", password_hash=DEMO_PASSWORD,
                         role="admin", is_active=True, email_verified=True)
            db.session.add(admin)
            db.session.flush()
            print("  ✅ Admin created")

        # ── Students ───────────────────────────────────
        student_users = []
        for s in STUDENTS:
            if not User.query.filter_by(email=s["email"]).first():
                u = User(name=s["name"], email=s["email"], password_hash=DEMO_PASSWORD,
                         role="student", is_active=True, email_verified=True)
                db.session.add(u)
                db.session.flush()
                st = Student(user_id=u.id, department=s["department"], year=s["year"],
                             skills=s["skills"], interests=s["interests"], bio=s["bio"],
                             github_url=s.get("github_url"), linkedin_url=s.get("linkedin_url"))
                db.session.add(st)
                # Points
                pts = UserPoints(user_id=u.id, total=random.randint(100,800),
                                 mentoring=random.randint(0,200), posting=random.randint(50,300),
                                 helping=random.randint(20,150), engagement=random.randint(30,150))
                db.session.add(pts)
                student_users.append(u)
            else:
                student_users.append(User.query.filter_by(email=s["email"]).first())
        db.session.commit()
        print(f"  ✅ {len(student_users)} students ready")

        # ── Alumni ─────────────────────────────────────
        alumni_users = []
        alumni_profiles = []
        for a in ALUMNI:
            if not User.query.filter_by(email=a["email"]).first():
                u = User(name=a["name"], email=a["email"], password_hash=DEMO_PASSWORD,
                         role="alumni", is_active=True, email_verified=True)
                db.session.add(u)
                db.session.flush()
                al = Alumni(user_id=u.id, company=a["company"], job_role=a["job_role"],
                            graduation_year=a["graduation_year"], location=a["location"],
                            skills=a["skills"], bio=a["bio"], domain=a["domain"],
                            mentorship_slots=a["mentorship_slots"], is_hiring=a["is_hiring"],
                            linkedin=a["linkedin"], impact_score=a["impact_score"],
                            mentorship_score=a["mentorship_score"])
                db.session.add(al)
                # Badges for alumni
                badges = [("top_mentor","Top Mentor","🏆"), ("active_contributor","Active Contributor","⭐")]
                for btype, bname, bicon in random.sample(badges, 1):
                    b = UserBadge(user_id=u.id, badge_type=btype, badge_name=bname, badge_icon=bicon)
                    db.session.add(b)
                pts = UserPoints(user_id=u.id, total=random.randint(500,2000),
                                 mentoring=random.randint(200,800), posting=random.randint(100,500))
                db.session.add(pts)
                alumni_users.append(u)
                alumni_profiles.append(al)
            else:
                u = User.query.filter_by(email=a["email"]).first()
                alumni_users.append(u)
                al = Alumni.query.filter_by(user_id=u.id).first()
                if al:
                    alumni_profiles.append(al)
        db.session.commit()
        print(f"  ✅ {len(alumni_users)} alumni ready")

        # ── Mentorship Requests ─────────────────────────
        all_students  = Student.query.all()
        all_alumni_p  = Alumni.query.all()
        statuses = ["accepted","accepted","accepted","pending","pending","rejected"]
        count = 0
        for student in all_students:
            chosen = random.sample(all_alumni_p, min(3, len(all_alumni_p)))
            for al in chosen:
                if not MentorshipRequest.query.filter_by(student_id=student.id, alumni_id=al.id).first():
                    req = MentorshipRequest(
                        student_id=student.id, alumni_id=al.id,
                        status=random.choice(statuses),
                        message=f"Hi! I'm a {student.year} year {student.department} student. I'd love to learn from your experience at {al.company}.",
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1,90))
                    )
                    db.session.add(req)
                    count += 1
        db.session.commit()
        print(f"  ✅ {count} mentorship requests seeded")

        # ── Posts ──────────────────────────────────────
        all_users = student_users + alumni_users
        post_objects = []
        for i, pd in enumerate(POSTS_DATA):
            user = all_users[i % len(all_users)]
            if not Post.query.filter_by(user_id=user.id, post_type=pd["type"]).first():
                post = Post(
                    user_id=user.id, content=pd["content"],
                    post_type=pd["type"], tags=pd["tags"],
                    likes_count=random.randint(5, 280),
                    comments_count=random.randint(1, 45),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0,30), hours=random.randint(0,23))
                )
                db.session.add(post)
                post_objects.append(post)
        db.session.commit()
        print(f"  ✅ {len(post_objects)} posts seeded")

        # ── Communities ────────────────────────────────
        comm_objects = []
        for cd in COMMUNITIES:
            if not Community.query.filter_by(slug=cd["slug"]).first():
                c = Community(
                    name=cd["name"], slug=cd["slug"], icon=cd["icon"],
                    description=cd["description"], member_count=cd["member_count"],
                    post_count=cd["post_count"], is_active=True
                )
                db.session.add(c)
                comm_objects.append(c)
        db.session.flush()
        # Add random members
        all_communities = Community.query.all()
        for user in all_users:
            chosen_comms = random.sample(all_communities, min(3, len(all_communities)))
            for c in chosen_comms:
                if not CommunityMember.query.filter_by(community_id=c.id, user_id=user.id).first():
                    m = CommunityMember(community_id=c.id, user_id=user.id)
                    db.session.add(m)
        db.session.commit()
        print(f"  ✅ {len(all_communities)} communities with members seeded")

        # ── Jobs ───────────────────────────────────────
        for jd in JOBS_DATA:
            # Find an alumni who works at that company to post it
            poster = next((u for u in alumni_users if jd["company"] in
                           (Alumni.query.filter_by(user_id=u.id).first() or Alumni()).company or ""), alumni_users[0])
            if not Job.query.filter_by(title=jd["title"], company=jd["company"]).first():
                job = Job(
                    posted_by=poster.id, title=jd["title"], company=jd["company"],
                    location=jd["location"], job_type=jd["job_type"],
                    description=jd["description"], requirements=jd["requirements"],
                    skills_required=jd["skills_required"], salary_range=jd["salary_range"],
                    is_active=True, views=random.randint(50, 500),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 14))
                )
                db.session.add(job)
        db.session.commit()
        print(f"  ✅ {len(JOBS_DATA)} jobs seeded")

        # ── Projects ───────────────────────────────────
        for i, pd in enumerate(PROJECTS_DATA):
            user = all_users[i % len(all_users)]
            if not ProjectShowcase.query.filter_by(title=pd["title"]).first():
                proj = ProjectShowcase(
                    user_id=user.id, title=pd["title"], description=pd["description"],
                    tech_stack=pd["tech_stack"], github_url=pd["github_url"],
                    demo_url=pd.get("demo_url"), likes_count=pd["likes_count"],
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 60))
                )
                db.session.add(proj)
        db.session.commit()
        print(f"  ✅ {len(PROJECTS_DATA)} projects seeded")

        # ── Notifications ──────────────────────────────
        notif_templates = [
            ("mentor_accepted",   "Mentorship Accepted! 🎉", "{} accepted your mentorship request."),
            ("mentor_request",    "New Mentorship Request",  "{} sent you a mentorship request."),
            ("post_like",         "Someone liked your post", "{} liked your post."),
            ("new_job",           "New Job Opportunity 💼",  "A new {} role was posted by {}."),
            ("community_join",    "Community Update",        "{} joined your community."),
        ]
        for user in all_users[:8]:  # Give notifications to first 8 users
            for _ in range(random.randint(3, 8)):
                ntype, title, msg_tmpl = random.choice(notif_templates)
                other = random.choice([u for u in all_users if u.id != user.id])
                n = Notification(
                    user_id=user.id, type=ntype, title=title,
                    message=msg_tmpl.format(other.name, "SDE"),
                    is_read=random.choice([True, True, False]),
                    created_at=datetime.utcnow() - timedelta(hours=random.randint(1, 72))
                )
                db.session.add(n)
        db.session.commit()
        print("  ✅ Notifications seeded")

        print("\n" + "="*55)
        print("🎉 AI CareerVerse V3 seed complete!")
        print("="*55)
        print("\n📋 Demo Credentials:")
        print("  👤 Student:  student@demo.com  / Demo@1234")
        print("  💼 Alumni:   alumni@demo.com   / Demo@1234")
        print("  ⚙️  Admin:    admin@demo.com    / Demo@1234")
        print("\n  All 20 demo users use password: Demo@1234")
        print("="*55)


if __name__ == "__main__":
    seed()
