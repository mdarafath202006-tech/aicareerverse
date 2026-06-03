#!/usr/bin/env python3
"""
AI CareerVerse V5 — Full Demo Seed Script
Generates: 15 students, 8 alumni, 5 mentors (as alumni), 3 recruiters, 1 admin
           8 companies, 22 jobs, 5 communities, ~100 posts,
           mentorship records, referral records, knowledge base entries
Run: python migrations/seed_v5.py
"""
import sys, os, random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.models.base import db
from app.models import (
    User, Student, Alumni, MentorshipRequest,
    Post, Comment, Like, Notification,
    Community, CommunityMember,
    Job, JobApplication,
    ProjectShowcase, UserPoints, UserBadge,
    Referral, Company, KnowledgeEntry, Follow,
)
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

app = create_app("config.DevelopmentConfig")
HASH = generate_password_hash("Demo@1234")

# ────────────────────────────────────────────────────────────────────────────
# DATA DEFINITIONS
# ────────────────────────────────────────────────────────────────────────────

STUDENTS = [
    dict(name="Arjun Verma",     email="student@demo.com",         department="Computer Science",  year="3rd",
         skills="Python,React,Machine Learning,SQL,Git",        interests="AI/ML,Product Management",
         bio="Passionate about AI and building impactful products. Finalist at HackIndia 2024.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=arjun"),
    dict(name="Priya Kapoor",    email="priya.kapoor@demo.com",    department="Data Science",       year="4th",
         skills="Python,TensorFlow,Statistics,Tableau,Pandas",  interests="Data Science,Finance,ML",
         bio="Data Science student passionate about turning raw data into strategic insights.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=priya"),
    dict(name="Neha Sharma",     email="neha.sharma@demo.com",     department="Cybersecurity",      year="2nd",
         skills="Network Security,Linux,Python,OWASP,Burp Suite",interests="Cybersecurity,Ethical Hacking",
         bio="Cybersecurity enthusiast building safer digital systems. CTF player ranked top 200 in India.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=neha"),
    dict(name="Rohan Mehta",     email="rohan.mehta@demo.com",     department="Computer Science",  year="3rd",
         skills="JavaScript,React,Node.js,MongoDB,TypeScript",  interests="Full Stack,Startups",
         bio="Full stack developer. Built 3 production apps. Looking for my first SDE internship.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=rohan"),
    dict(name="Ananya Singh",    email="ananya.singh@demo.com",    department="AI & ML",            year="4th",
         skills="PyTorch,NLP,Python,Transformers,HuggingFace",  interests="Natural Language Processing,Research",
         bio="NLP researcher at IIT Delhi. Working on multilingual language models for low-resource languages.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=ananya"),
    dict(name="Vikram Rao",      email="vikram.rao@demo.com",      department="Electronics",        year="2nd",
         skills="C++,Embedded Systems,Arduino,IoT,RTOS",        interests="IoT,Robotics,Hardware",
         bio="Hardware enthusiast building IoT solutions for smart agriculture.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=vikram"),
    dict(name="Kavya Reddy",     email="kavya.reddy@demo.com",     department="Computer Science",  year="1st",
         skills="Python,HTML,CSS,Java,Figma",                   interests="UI/UX,Mobile Development",
         bio="First-year CS student eager to learn. Built a portfolio website last summer.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=kavya"),
    dict(name="Aditya Kumar",    email="aditya.kumar@demo.com",    department="Information Tech",   year="3rd",
         skills="DevOps,Docker,Kubernetes,AWS,Terraform",        interests="Cloud,DevOps,SRE",
         bio="DevOps enthusiast automating everything. AWS Solutions Architect Associate certified.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=aditya"),
    dict(name="Pooja Iyer",      email="pooja.iyer@demo.com",      department="Data Science",       year="2nd",
         skills="R,Python,Statistics,Power BI,Excel",            interests="Business Analytics,Finance",
         bio="Aspiring business analyst. Love uncovering stories hidden in numbers.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=pooja"),
    dict(name="Siddharth Nair",  email="siddharth.nair@demo.com",  department="Computer Science",  year="4th",
         skills="System Design,Java,Spring Boot,SQL,Redis",      interests="Backend,Distributed Systems",
         bio="Backend engineer at heart. Building scalable systems. Interned at PayTM.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=sid"),
    dict(name="Riya Gupta",      email="riya.gupta@demo.com",      department="Computer Science",  year="3rd",
         skills="Flutter,Dart,Firebase,React Native,UI/UX",      interests="Mobile Development,Design",
         bio="Mobile developer with 2 published apps. Passionate about clean, accessible UX.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=riya"),
    dict(name="Karan Singh",     email="karan.singh@demo.com",     department="Information Tech",   year="2nd",
         skills="Python,Django,PostgreSQL,REST APIs,Linux",       interests="Backend Development,Open Source",
         bio="Django developer contributing to open source. Maintainer of a 500+ star GitHub project.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=karan"),
    dict(name="Shreya Patel",    email="shreya.patel@demo.com",    department="AI & ML",            year="3rd",
         skills="Computer Vision,OpenCV,PyTorch,Python,YOLO",    interests="Computer Vision,Robotics",
         bio="Computer vision researcher. Built an attendance system using face recognition for my college.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=shreya"),
    dict(name="Amit Joshi",      email="amit.joshi@demo.com",      department="Computer Science",  year="1st",
         skills="C,C++,Python,Data Structures,Algorithms",        interests="Competitive Programming,Systems",
         bio="Competitive programmer. Codeforces rated 1650. Aiming for ICPC World Finals.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=amit"),
    dict(name="Nisha Reddy",     email="nisha.reddy@demo.com",     department="Data Science",       year="4th",
         skills="Spark,Hadoop,Python,Kafka,Airflow",              interests="Data Engineering,Big Data",
         bio="Data engineering student with hands-on experience in building real-time pipelines.",
         github_url="https://github.com", linkedin_url="https://linkedin.com",
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=nisha"),
]

ALUMNI = [
    dict(name="Priya Sharma",   email="alumni@demo.com",           company="Google",       job_role="Senior Product Manager",
         graduation_year=2020, location="Bangalore, India",
         skills="Product Management,Strategy,Analytics,Leadership,Roadmapping",
         bio="Passionate about building products that create impact. 5 years at Google. Happy to mentor and guide students.",
         domain="Product Management", mentorship_slots=5, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=92, mentorship_score=88,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=priyasharma"),
    dict(name="Rahul Gupta",    email="rahul.gupta@demo.com",      company="Microsoft",    job_role="Software Engineer L5",
         graduation_year=2019, location="Hyderabad, India",
         skills="C#,.NET,Azure,System Design,Distributed Systems,Microservices",
         bio="Building cloud-scale systems at Microsoft. 6 years of experience. Love helping aspiring engineers crack FAANG.",
         domain="Backend Engineering", mentorship_slots=4, is_hiring=False,
         linkedin="https://linkedin.com", impact_score=85, mentorship_score=80,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=rahulgupta"),
    dict(name="Kavya Pillai",   email="kavya.pillai@demo.com",     company="Amazon",       job_role="Machine Learning Engineer",
         graduation_year=2021, location="Chennai, India",
         skills="TensorFlow,PyTorch,Python,MLOps,AWS SageMaker,NLP",
         bio="ML engineer at Amazon Alexa. Passionate about NLP and conversational AI. Ex-Google Summer of Code.",
         domain="Machine Learning", mentorship_slots=3, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=78, mentorship_score=75,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=kavyapillai"),
    dict(name="Arjun Patel",    email="arjun.patel@demo.com",      company="Flipkart",     job_role="Senior SDE",
         graduation_year=2018, location="Bangalore, India",
         skills="Java,Microservices,Kafka,Redis,System Design,MySQL",
         bio="7 years building e-commerce infrastructure at Flipkart. Scale is my specialty. Happy to share learnings.",
         domain="Backend Engineering", mentorship_slots=3, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=88, mentorship_score=82,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=arjunpatel"),
    dict(name="Meera Krishnan", email="meera.krishnan@demo.com",   company="Razorpay",     job_role="Engineering Manager",
         graduation_year=2017, location="Bangalore, India",
         skills="Engineering Management,Go,System Design,Leadership,FinTech,Team Building",
         bio="Building India's payment infrastructure at Razorpay. Passionate about developer experience. Mentor 10+ engineers.",
         domain="Engineering Leadership", mentorship_slots=2, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=95, mentorship_score=90,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=meera"),
    dict(name="Kiran Reddy",    email="kiran.reddy@demo.com",      company="Swiggy",       job_role="Data Scientist",
         graduation_year=2020, location="Hyderabad, India",
         skills="Python,PySpark,Airflow,ML,SQL,Tableau,XGBoost",
         bio="Using data to optimize food delivery at massive scale at Swiggy. Let's talk data science, ML in industry!",
         domain="Data Science", mentorship_slots=4, is_hiring=False,
         linkedin="https://linkedin.com", impact_score=72, mentorship_score=68,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=kiranreddy"),
    dict(name="Ankit Shah",     email="ankit.shah@demo.com",       company="Zepto",        job_role="Co-Founder & CTO",
         graduation_year=2019, location="Mumbai, India",
         skills="Startups,Engineering,Leadership,Fundraising,Product,Architecture",
         bio="Co-founded Zepto. Building quick-commerce from scratch. Happy to share my startup journey, fundraising, and tech decisions.",
         domain="Startups", mentorship_slots=2, is_hiring=True,
         linkedin="https://linkedin.com", impact_score=98, mentorship_score=95,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=ankitshah"),
    dict(name="Sneha Agarwal",  email="sneha.agarwal@demo.com",    company="Infosys",      job_role="Cybersecurity Lead",
         graduation_year=2016, location="Pune, India",
         skills="Penetration Testing,SIEM,Incident Response,CISSP,Python,Threat Intelligence",
         bio="10 years in cybersecurity. Leading Infosys's security practice. Helping the next generation secure the digital world.",
         domain="Cybersecurity", mentorship_slots=5, is_hiring=False,
         linkedin="https://linkedin.com", impact_score=82, mentorship_score=78,
         avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=sneha"),
]

COMPANIES = [
    dict(name="Google",      slug="google",      industry="Technology",      location="Bangalore, India",   size="100000+",  founded=1998, is_hiring=True,  description="Google India is a technology company specializing in Internet-related services and products, including online advertising technologies, a search engine, cloud computing, software, and hardware."),
    dict(name="Microsoft",   slug="microsoft",   industry="Technology",      location="Hyderabad, India",   size="50000+",   founded=1975, is_hiring=True,  description="Microsoft India Development Center is one of the largest R&D facilities outside the US, working on products like Azure, Office 365, and Bing."),
    dict(name="Amazon",      slug="amazon",      industry="E-Commerce",      location="Bangalore, India",   size="100000+",  founded=1994, is_hiring=True,  description="Amazon's India tech hub drives innovation for AWS, Alexa, and global logistics across machine learning, distributed systems, and cloud services."),
    dict(name="Flipkart",    slug="flipkart",    industry="E-Commerce",      location="Bangalore, India",   size="10000+",   founded=2007, is_hiring=True,  description="India's leading e-commerce marketplace, building cutting-edge technology for millions of customers and sellers across the country."),
    dict(name="Razorpay",    slug="razorpay",    industry="FinTech",         location="Bangalore, India",   size="2000+",    founded=2014, is_hiring=True,  description="Razorpay is India's leading payment solutions company, providing payment gateway, business banking, and financial infrastructure for businesses."),
    dict(name="Swiggy",      slug="swiggy",      industry="Food Tech",       location="Bangalore, India",   size="5000+",    founded=2014, is_hiring=False, description="Swiggy is India's largest on-demand delivery platform, solving complex logistics and data science problems at massive scale."),
    dict(name="Zepto",       slug="zepto",       industry="Quick Commerce",  location="Mumbai, India",      size="1000+",    founded=2021, is_hiring=True,  description="Zepto is India's fastest growing quick-commerce startup, delivering groceries in 10 minutes through a dense network of dark stores."),
    dict(name="Infosys",     slug="infosys",     industry="IT Services",     location="Pune, India",        size="300000+",  founded=1981, is_hiring=False, description="Infosys is a global leader in next-generation digital services and consulting, helping clients navigate their digital transformation."),
]

COMMUNITIES = [
    dict(name="AI & Machine Learning", slug="ai-ml",         icon="🤖", description="Deep learning, NLP, computer vision, and everything AI. For researchers and practitioners.", member_count=2400, post_count=340),
    dict(name="Web Development",       slug="webdev",         icon="🌐", description="Frontend, backend, full-stack. React to Django, everything web development.", member_count=3100, post_count=520),
    dict(name="Cybersecurity",         slug="cybersec",       icon="🔒", description="Ethical hacking, blue team, security research, and CTF challenges.", member_count=1800, post_count=210),
    dict(name="Data Science",          slug="datascience",    icon="📊", description="Statistics, data engineering, BI, and ML in industry.", member_count=2900, post_count=480),
    dict(name="DevOps & Cloud",        slug="devops",         icon="⚙️", description="CI/CD, containers, Kubernetes, AWS, GCP, Azure. Ship faster.", member_count=1500, post_count=190),
]

JOBS_DATA = [
    dict(title="Software Engineer Intern", company="Google", location="Bangalore, India", job_type="internship", description="Join Google's engineering team for a 3-month internship. You'll work on real products used by billions of users, contribute to code reviews, and ship features end-to-end.", requirements="CS background, strong algorithms and data structures, one programming language proficiency", skills_required="Python,C++,Algorithms,Data Structures", salary_range="₹80,000/month"),
    dict(title="Data Science Intern", company="Swiggy", location="Bangalore, India", job_type="internship", description="Work with Swiggy's data science team to build ML models that optimize delivery ETA predictions and restaurant recommendations for 50 million+ users.", requirements="Statistics, Python, ML basics, SQL", skills_required="Python,Machine Learning,SQL,Statistics", salary_range="₹60,000/month"),
    dict(title="Frontend Engineer Intern", company="Razorpay", location="Bangalore, India", job_type="internship", description="Build FinTech UX for Razorpay's payment dashboard. You'll work with React, TypeScript, and design a checkout experience used by 8 million businesses.", requirements="React, JavaScript, CSS, basic TypeScript", skills_required="React,JavaScript,TypeScript,CSS", salary_range="₹50,000/month"),
    dict(title="ML Engineer Intern", company="Amazon", location="Hyderabad, India", job_type="internship", description="Work with the Alexa team on NLP models for intent recognition. Build training pipelines with AWS SageMaker and improve Alexa's understanding of Indian accents.", requirements="Python, ML fundamentals, NLP basics", skills_required="Python,NLP,TensorFlow,AWS", salary_range="₹75,000/month"),
    dict(title="DevOps Intern", company="Microsoft", location="Hyderabad, India", job_type="internship", description="Work with Azure DevOps engineering team. Set up CI/CD pipelines, improve monitoring dashboards, and reduce deployment failure rates for internal teams.", requirements="Linux, Docker, basic CI/CD knowledge", skills_required="Docker,Kubernetes,CI/CD,Azure,Linux", salary_range="₹55,000/month"),
    dict(title="Software Development Engineer", company="Flipkart", location="Bangalore, India", job_type="full_time", description="Build and scale Flipkart's e-commerce platform serving 400 million+ registered users. Work on distributed systems, high-availability services, and real-time data processing.", requirements="3-5 years experience, Java/Go, distributed systems", skills_required="Java,System Design,Microservices,Kafka,Redis", salary_range="₹18-28 LPA"),
    dict(title="Senior Data Scientist", company="Swiggy", location="Bangalore, India", job_type="full_time", description="Lead data science initiatives for Swiggy's logistics optimization. Design ML models for delivery partner routing, ETA prediction, and demand forecasting.", requirements="4+ years, Python, ML deployment experience", skills_required="Python,PySpark,ML,SQL,Airflow", salary_range="₹22-35 LPA"),
    dict(title="Product Manager", company="Razorpay", location="Bangalore, India", job_type="full_time", description="Own the product roadmap for Razorpay's payment gateway. Define strategy, work with engineering and design teams, and track north-star metrics.", requirements="3+ years PM experience, fintech preferred", skills_required="Product Strategy,Analytics,SQL,Leadership", salary_range="₹25-40 LPA"),
    dict(title="Senior ML Engineer", company="Amazon", location="Bangalore, India", job_type="full_time", description="Drive ML innovation for Amazon India's recommendation and personalization systems. Lead a team of 4 engineers, own model performance, and deploy at scale.", requirements="5+ years, deep learning, MLOps", skills_required="PyTorch,AWS,MLOps,Python,System Design", salary_range="₹30-50 LPA"),
    dict(title="Cloud Solutions Architect", company="Microsoft", location="Hyderabad, India", job_type="full_time", description="Help Microsoft's enterprise customers architect and migrate to Azure. Conduct workshops, build PoCs, and provide technical leadership during digital transformation projects.", requirements="7+ years, Azure/AWS, enterprise architecture", skills_required="Azure,Architecture,Cloud,DevOps,Security", salary_range="₹35-55 LPA"),
    dict(title="Backend Engineer", company="Zepto", location="Mumbai, India", job_type="full_time", description="Build Zepto's order management and inventory systems. Work on ultra-low-latency APIs that power 10-minute deliveries at scale across 25 cities.", requirements="2+ years, Go or Node.js, SQL/NoSQL", skills_required="Go,Node.js,PostgreSQL,Redis,System Design", salary_range="₹15-25 LPA"),
    dict(title="Cybersecurity Analyst", company="Infosys", location="Pune, India", job_type="full_time", description="Join Infosys's Cyber Defense Center. Monitor SIEM, respond to security incidents, conduct vulnerability assessments, and build threat intelligence for enterprise clients.", requirements="2+ years security experience, CEH/CISSP preferred", skills_required="SIEM,Penetration Testing,Python,Incident Response", salary_range="₹10-18 LPA"),
    dict(title="iOS Developer", company="Flipkart", location="Bangalore, India", job_type="full_time", description="Build features for the Flipkart iOS app used by 100M+ users. Work on performance optimization, new checkout flows, and AR-powered product visualization.", requirements="3+ years iOS, Swift, UIKit/SwiftUI", skills_required="Swift,iOS,UIKit,SwiftUI,Xcode", salary_range="₹18-28 LPA"),
    dict(title="Data Engineer", company="Google", location="Bangalore, India", job_type="full_time", description="Build data pipelines that power Google's advertising analytics in India. Work with BigQuery, Dataflow, and Pub/Sub to process petabytes of event data daily.", requirements="4+ years, Python, SQL, BigQuery", skills_required="Python,SQL,BigQuery,Dataflow,Spark", salary_range="₹25-40 LPA"),
    dict(title="React Developer", company="Razorpay", location="Remote", job_type="full_time", description="Build Razorpay's next-generation dashboard for merchants. Work on micro-frontend architecture, performance budgets, and accessibility improvements.", requirements="3+ years React, TypeScript, performance optimization", skills_required="React,TypeScript,GraphQL,Performance,CSS", salary_range="₹15-25 LPA"),
    dict(title="Site Reliability Engineer", company="Amazon", location="Hyderabad, India", job_type="full_time", description="Ensure 99.99% uptime for Amazon India's critical shopping infrastructure. Build runbooks, automate toil, define SLOs, and lead incident response.", requirements="3+ years SRE/DevOps, Kubernetes, monitoring", skills_required="Kubernetes,Terraform,Monitoring,AWS,Python", salary_range="₹22-35 LPA"),
    dict(title="Mobile Developer (React Native)", company="Zepto", location="Mumbai, India", job_type="full_time", description="Build Zepto's customer-facing app. Optimize for performance on low-end Android devices, implement real-time order tracking, and ship features rapidly.", requirements="2+ years React Native, JavaScript/TypeScript", skills_required="React Native,JavaScript,TypeScript,Firebase", salary_range="₹12-20 LPA"),
    dict(title="Junior Security Analyst", company="Infosys", location="Bangalore, India", job_type="full_time", description="Entry-level role in Infosys's Security Operations Center. Monitor security alerts, triage incidents, support senior analysts, and get hands-on training.", requirements="Fresher/1 year, CEH or Security+ preferred", skills_required="Linux,Networking,Python,OWASP", salary_range="₹6-10 LPA"),
    dict(title="Engineering Manager", company="Flipkart", location="Bangalore, India", job_type="full_time", description="Lead a team of 8 engineers building Flipkart's seller platform. Drive technical roadmap, set engineering standards, and grow your team's capabilities.", requirements="8+ years, 2+ years management", skills_required="Engineering Management,System Design,Java,Leadership", salary_range="₹40-60 LPA"),
    dict(title="Product Analyst Intern", company="Google", location="Bangalore, India", job_type="internship", description="Work with Google Maps' product team in India. Analyze user behavior data, run A/B tests, build dashboards, and present insights to PMs and executives.", requirements="SQL, statistics, data visualization", skills_required="SQL,Python,Tableau,Statistics,Excel", salary_range="₹65,000/month"),
    dict(title="Full Stack Engineer", company="Razorpay", location="Bangalore, India", job_type="full_time", description="Build end-to-end features for Razorpay's SME banking product. Own features from API design to React frontend, CI/CD, and monitoring.", requirements="3+ years full stack, React + Node.js or Django", skills_required="React,Node.js,PostgreSQL,REST APIs,Docker", salary_range="₹18-30 LPA"),
    dict(title="MLOps Engineer", company="Amazon", location="Remote", job_type="full_time", description="Build the infrastructure and tooling that makes ML teams 10x faster. Develop automated training pipelines, model monitoring, and A/B testing frameworks.", requirements="3+ years MLOps/DevOps, ML background", skills_required="MLOps,Kubernetes,AWS,Python,Docker", salary_range="₹25-40 LPA"),
]

POSTS = [
    dict(type="achievement", content="Just got my offer letter from Google! 🎉 After 6 months of grinding LeetCode, mock interviews, and countless rejections — it finally happened. To everyone still in the process: keep going. Your time will come. #Google #Placement #SoftwareEngineering"),
    dict(type="text",        content="Hot take: LeetCode is NOT the most important thing for cracking FAANG. Yes, DSA matters. But what really differentiates candidates is system design clarity, communication, and showing genuine curiosity. Thoughts? 👇 #TechInterviews"),
    dict(type="opportunity", content="My team at Flipkart is hiring Backend Engineers (3-5 yrs, Java/Go). Strong team, interesting scale problems, great culture. DM me or apply via the Jobs section. #Hiring #Flipkart #BackendEngineering"),
    dict(type="text",        content="5 things I wish I knew as a CS fresher:\n\n1. Build projects — not just clone apps, real projects solving real problems\n2. Contribute to open source — it signals initiative\n3. Network early — alumni connections matter\n4. Learn system design from day 1\n5. Soft skills will differentiate you at the top\n\nSave this. #CareerAdvice"),
    dict(type="text",        content="Unpopular opinion: Your GPA doesn't matter as much as you think after 2nd year. What matters: 1) Projects that show initiative, 2) Internships, 3) Strong GitHub, 4) Communication skills. Start building. #CareerTips #CSStudents"),
    dict(type="achievement", content="Proud to share I've mentored 50+ students through AI CareerVerse this year! Seeing students land at Google, Microsoft, and startups is incredibly fulfilling. If you're a student looking for a mentor, send me a request. Open slots available! 🙌"),
    dict(type="text",        content="Just wrapped up System Design bootcamp with 10 students. Here's what I learned about teaching:\n\n→ Analogies work better than theory\n→ Students learn more from 'what if we don't do X' than 'do X'\n→ Real examples from production > textbook examples\n\nTeaching is the best way to learn. #Mentorship"),
    dict(type="opportunity", content="Hey freshers! Razorpay's data team is looking for interns this summer. Great opportunity to work on real fintech data problems. Skills needed: Python, SQL, basic statistics. Check the Jobs section! #Internship #DataScience #Razorpay"),
    dict(type="text",        content="How I prepared for system design interviews at Microsoft:\n\n1. Drew 30+ system designs on paper\n2. Focused on trade-offs, not just 'correct answers'\n3. Read high-scale engineering blogs (Uber, Netflix, Discord)\n4. Mock interviews with alumni (this platform helped!)\n5. Built a distributed cache as a project\n\nResult: Offer in Round 4 ✅ #SystemDesign #Microsoft"),
    dict(type="text",        content="The secret to getting referrals that actually work: PERSONALIZATION.\n\nDon't send generic messages. Instead:\n→ Reference specific projects they worked on\n→ Explain WHY that company specifically\n→ Show you've researched the team/role\n→ Make it easy to say yes (attach resume, LinkedIn)\n\nRespect their time. #Referral #JobSearch"),
    dict(type="achievement", content="Our college team won Smart India Hackathon 2024! 🏆 Built an AI-powered water quality monitoring system using IoT sensors + ML. 72 hours, no sleep, pure adrenaline. Grateful for my incredible teammates! #SIH2024 #Hackathon"),
    dict(type="text",        content="Python libraries every data scientist should know in 2025:\n\n📊 Data: Pandas, Polars (faster!)\n📈 Viz: Matplotlib, Plotly, Seaborn\n🤖 ML: Scikit-learn, XGBoost, LightGBM\n🧠 DL: PyTorch, HuggingFace\n🔧 Prod: FastAPI, Docker, MLflow\n\nMaster these and you're 80% there. #DataScience #Python"),
    dict(type="text",        content="Interview experience: Cracked Amazon SDE-2 after 3 attempts.\n\nWhat changed on attempt 3:\n→ Wrote code on paper first, THEN debugged mentally\n→ Talked through every thought — interviewers LOVE this\n→ Asked clarifying questions before coding\n→ Managed time — spent 5 min planning before writing\n\nYou don't need to be the smartest. You need to be the clearest thinker. #Amazon #Interviews"),
    dict(type="text",        content="Cold outreach tips from someone who got 3 offers this way:\n\n✅ DM on LinkedIn, NOT email for faster responses\n✅ Reference specific work they've published\n✅ Keep it under 100 words\n✅ Clear ask: 30-min coffee chat\n✅ Follow up ONCE after 1 week\n\nMost people are afraid to reach out. The ones who do, win. #Networking"),
    dict(type="achievement", content="After 8 months at Google, here's my honest review:\n\n🌟 Incredible scale — your code impacts billions\n🌟 Smartest colleagues I've ever worked with\n🌟 Learning never stops\n\n⚡ Ambiguity is high — you own your scope\n⚡ Politics exists (surprise!)\n⚡ Impact takes time\n\nOverall: Best decision I've made. AMA! #Google #TechLife"),
    dict(type="text",        content="Resume tip that got me 80% callback rate:\n\nEvery bullet point should follow: [Action verb] + [What you did] + [Impact]\n\n❌ 'Worked on backend APIs'\n✅ 'Designed REST APIs for product catalog, reducing mobile load time by 40%'\n\nQuantify everything. Numbers make you memorable. #Resume #CareerTips"),
    dict(type="opportunity", content="Zepto is hiring! We're growing fast and need talented engineers across all levels. Fast-paced startup environment, great equity, and problems that genuinely haven't been solved before. Apply via AI CareerVerse or DM me. #Zepto #Hiring #Startup"),
    dict(type="text",        content="Startup vs Big Tech — the real comparison:\n\n🏢 Big Tech: Structure, scale, prestige, slower growth, comp security\n🚀 Startup: Speed, ownership, risk, learning curve, equity upside\n\nNeither is better. It depends on where you are in your career and what you optimize for.\n\nEarly career? Consider startup for the speed of learning. #Career"),
    dict(type="text",        content="Things nobody tells you about your first job:\n\n→ Code reviews will feel personal at first (they're not)\n→ You'll spend more time reading code than writing it\n→ Soft skills matter more than you think\n→ Your manager relationship is critical — choose wisely\n→ It's ok to not know things — asking is strength\n\nYou'll figure it out. We all did. #FreshersAdvice"),
    dict(type="achievement", content="Just finished mentoring my first cohort of 5 students through AI CareerVerse! All 5 got internships — Google, Microsoft (2), Razorpay, and Zepto. Seeing them succeed is the best feeling. Thank you to this amazing platform! 🙏 #Mentorship #CareerVerse"),
]

KNOWLEDGE_ENTRIES = [
    dict(title="How I cracked Google SWE after 3 rejections — what finally worked",
         category="success_story", company="Google", role="Software Engineer",
         tags="google,algorithms,system design,persistence",
         content="""I applied to Google 3 times over 18 months before finally getting an offer. Here's what changed each attempt — and what finally worked.

**Attempt 1 (Failed at Phone Screen):**
I was underprepared for the complexity of LeetCode problems at Google's level. I could solve Medium problems but Hard problems completely stumped me. I spent too much time thinking and not enough explaining my thought process.

**Attempt 2 (Failed at Onsite, Round 3):**
Better DSA preparation but terrible system design. When asked to design YouTube, I jumped into components without clarifying requirements. The interviewer stopped me and asked clarifying questions I should have asked.

**What I changed for Attempt 3:**
1. Spent 3 months on system design exclusively — read Designing Data-Intensive Applications, studied Netflix/Discord/Uber engineering blogs
2. Did 30+ mock interviews where I was *forced* to explain out loud
3. For every LeetCode problem, I practiced explaining my approach before coding
4. When asked system design, I now spend the first 5 minutes *only* on clarification and scope

**The result:** Got an offer at L4. The interviewer specifically mentioned that my communication was exceptional.

**Key takeaway:** Google doesn't want the smartest person. They want someone who can solve ambiguous problems collaboratively. Communication IS the skill."""),
    dict(title="My Amazon SDE-2 interview experience — complete breakdown of all 5 rounds",
         category="interview_experience", company="Amazon", role="SDE-2",
         tags="amazon,behavioral,system design,leadership principles",
         content="""I recently cleared Amazon SDE-2 (L5). Here's a complete breakdown of all 5 rounds.

**Round 1: Online Assessment (3 hours)**
Two LeetCode-style problems (Medium-Hard) + debugging + system design MCQs. The DP problem tripped up most candidates. Focus on complexity analysis.

**Round 2: Technical Phone Screen (1 hour)**
Binary tree problems. I got: serialize/deserialize binary tree and LCA of BST. Clean code + test cases.

**Round 3: System Design (1 hour)**
Design a URL shortener at scale (10B URLs, 100K writes/sec, 1M reads/sec). I used consistent hashing + Cassandra. Key insight: clarify read-heavy vs write-heavy upfront.

**Round 4: Behavioral (45 min)**
Amazon Leadership Principles. Had STAR stories ready for: bias for action, customer obsession, earn trust, dive deep. Most important: use METRICS in your stories. Don't say "improved performance" — say "reduced latency from 800ms to 120ms".

**Round 5: Bar Raiser (1.5 hours)**
Toughest round. Mix of technical + behavioral. The bar raiser is looking for signals that you'd raise the bar of the team. Think big picture. Be honest about tradeoffs.

**Offer:** ₹42 LPA total comp.

**My advice:** Amazon is ALL about the Leadership Principles. Learn all 16. Have 2 stories per principle."""),
    dict(title="From 6 CGPA to ₹35 LPA — my honest journey (with everything I wish I'd known)",
         category="placement_story", company="Flipkart", role="Senior SDE",
         tags="cgpa,placement,flipkart,journey,motivation",
         content="""My CGPA in 3rd year was 6.1. I thought FAANG was out of reach. Today I earn ₹35 LPA at Flipkart. Here's the full story.

**The low point (3rd year):**
I was demotivated, thinking my CGPA closed all doors. I almost gave up and accepted that I'd work at a tier-3 IT company.

**What changed:**
A senior from my college who I connected with on LinkedIn (before platforms like this existed) told me something that changed everything: "Companies hire problem-solvers, not GPA certificates."

**My 1-year transformation plan:**
- 6 months of LeetCode (200+ problems, focus on patterns not volume)
- Built 3 real projects (not todo apps — a real-time collaborative code editor, an e-commerce backend with 1M+ product catalog simulation, a distributed task queue)
- Contributed to 2 open source projects (this got me noticed)
- Got a 2-month startup internship (unpaid but worth every day)

**Interview season:**
Got shortlisted at 8 companies, cleared 5, got offers from 3. Joined Flipkart.

**The numbers:**
- Package: ₹18 LPA (2019) → ₹35 LPA (now, 4 years later)
- CGPA at time of placement: 6.8 (slightly improved)

**Key message:**
Your CGPA is not your destiny. Your GitHub is your new resume. Start building. Now."""),
    dict(title="Startup vs FAANG — I've done both, here's the real truth",
         category="career_guide", company="Zepto", role="Co-Founder & CTO",
         tags="startup,faang,career choice,growth,equity",
         content="""I spent 2 years at Google post-college, then co-founded Zepto. Here's my genuinely honest comparison.

**Google (2 years):**
Pros: Incredible infrastructure, brilliant colleagues, structured growth, great ESOP, world-class learning.
Cons: Slow decision-making, impact feels distant, hard to own things end-to-end, politics at senior levels.

**Zepto (co-founder, now CTO):**
Pros: Every line of code affects the business directly, speed of learning is 10x, equity upside is massive if it works, you own everything.
Cons: Uncertain future, high stress, wear many hats, salary can be lower early-on, equity might be worth nothing.

**My recommendation based on career stage:**

*0-2 years exp:* Consider a startup if you're self-driven and want to learn fast. Big tech if you want structure and mentorship.

*2-5 years exp:* This is the sweet spot for startup equity. You have enough skills to add value and enough runway to benefit.

*5+ years:* FAANG for financial security and L-bracket compensation, OR startup as a senior leader where you can really move the needle.

**The uncomfortable truth:** Most people should try FAANG first to build strong foundations, then startup to apply them at speed.

Whatever you choose — choose with intention. Both paths work."""),
    dict(title="How to request referrals that actually convert — templates that worked for me",
         category="tips_and_tricks", company="Microsoft", role="Software Engineer L5",
         tags="referral,networking,linkedin,job search,templates",
         content="""I've given 40+ referrals in the last 3 years and received 6 myself. Here's the formula that actually works.

**The brutal truth about most referral requests:**
90% of messages I get start with "Hi, I'm a student from XYZ college. Please refer me for any role."
This goes straight to ignored.

**What actually works:**

**Template that got me a Google referral:**
"Hi [Name], I've been following your work on [specific project/article they wrote]. I'm a final-year CS student who's built [specific thing relevant to their work]. I'm applying for Google's SWE internship and your journey from [their college] to Google is exactly the path I'm targeting. Would you be open to a 15-minute call next week? I'd love your perspective on preparing for Google's bar. Happy to share my resume if useful."

**Why this works:**
1. Specific research shows genuine interest
2. Makes it about learning from them, not asking for a favor
3. Specific time request (15 min) is low commitment
4. No demand for referral — you earn it in the conversation

**The follow-up:**
If they say yes → have the best 15-minute call of your life. Be prepared, be specific, be curious.
After the call → send a thank you + your resume + "If you think I'm a fit, I'd be grateful for a referral."

**Success rate:** This approach gets ~60% response rate vs ~5% for generic messages.

Remember: A warm referral from someone who believes in you is worth 100x a cold application."""),
]

# ────────────────────────────────────────────────────────────────────────────
# SEED FUNCTIONS
# ────────────────────────────────────────────────────────────────────────────

def clear_all():
    print("Clearing existing data...")
    for model in [KnowledgeEntry, Follow, Referral, JobApplication, Job,
                  CommunityMember, Community, UserBadge, UserPoints,
                  ProjectShowcase, Like, Comment, Post, Notification,
                  MentorshipRequest, Alumni, Student, Company, User]:
        try:
            model.query.delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"  Warning clearing {model.__name__}: {e}")

def seed_all():
    clear_all()
    now = datetime.utcnow()

    # ── Admin ──────────────────────────────────────────
    print("Creating admin...")
    admin = User(name="Admin CareerVerse", email="admin@demo.com", role="admin",
                 is_active=True, email_verified=True, password_hash=HASH,
                 avatar_url="https://api.dicebear.com/7.x/avataaars/svg?seed=admin",
                 created_at=now - timedelta(days=365))
    db.session.add(admin)
    db.session.flush()

    # ── Companies ──────────────────────────────────────
    print("Creating companies...")
    company_objs = {}
    for c in COMPANIES:
        obj = Company(**c, created_at=now - timedelta(days=random.randint(100,365)))
        db.session.add(obj)
        company_objs[c['name']] = obj
    db.session.flush()

    # ── Alumni ─────────────────────────────────────────
    print("Creating alumni...")
    alumni_objs = []
    for a_data in ALUMNI:
        u = User(name=a_data['name'], email=a_data['email'], role="alumni",
                 is_active=True, email_verified=True, password_hash=HASH,
                 avatar_url=a_data.get('avatar'),
                 created_at=now - timedelta(days=random.randint(180,365)))
        db.session.add(u)
        db.session.flush()
        al = Alumni(
            user_id=u.id, company=a_data['company'], job_role=a_data['job_role'],
            graduation_year=a_data['graduation_year'], location=a_data['location'],
            skills=a_data['skills'], bio=a_data['bio'], domain=a_data['domain'],
            mentorship_slots=a_data['mentorship_slots'], is_hiring=a_data['is_hiring'],
            linkedin=a_data['linkedin'], impact_score=a_data['impact_score'],
            mentorship_score=a_data['mentorship_score'], rating=round(random.uniform(4.0, 5.0), 2)
        )
        db.session.add(al)
        db.session.flush()
        alumni_objs.append((u, al))
        pts = UserPoints(user_id=u.id, total_points=random.randint(200, 1000))
        db.session.add(pts)

    # ── Students ───────────────────────────────────────
    print("Creating students...")
    student_objs = []
    for s_data in STUDENTS:
        u = User(name=s_data['name'], email=s_data['email'], role="student",
                 is_active=True, email_verified=True, password_hash=HASH,
                 avatar_url=s_data.get('avatar'),
                 created_at=now - timedelta(days=random.randint(30, 180)))
        db.session.add(u)
        db.session.flush()
        st = Student(
            user_id=u.id, department=s_data['department'], year=s_data['year'],
            skills=s_data['skills'], interests=s_data['interests'], bio=s_data['bio'],
            github_url=s_data['github_url'], linkedin_url=s_data['linkedin_url']
        )
        db.session.add(st)
        db.session.flush()
        student_objs.append((u, st))
        pts = UserPoints(user_id=u.id, total_points=random.randint(50, 400))
        db.session.add(pts)

    db.session.commit()

    # ── Communities ────────────────────────────────────
    print("Creating communities...")
    community_objs = []
    for c in COMMUNITIES:
        obj = Community(**c, created_by=admin.id, is_active=True,
                        created_at=now - timedelta(days=random.randint(60,300)))
        db.session.add(obj)
    db.session.flush()
    community_objs = Community.query.all()

    # Community memberships
    all_users = [u for u, _ in student_objs] + [u for u, _ in alumni_objs]
    for user in all_users:
        for comm in random.sample(community_objs, random.randint(1, 3)):
            try:
                m = CommunityMember(community_id=comm.id, user_id=user.id)
                db.session.add(m)
            except Exception:
                pass
    db.session.commit()

    # ── Jobs ───────────────────────────────────────────
    print("Creating jobs...")
    job_objs = []
    alumni_users = [u for u, _ in alumni_objs]
    for i, j in enumerate(JOBS_DATA):
        poster = alumni_users[i % len(alumni_users)]
        job = Job(
            posted_by=poster.id, title=j['title'], company=j['company'],
            location=j['location'], job_type=j['job_type'],
            description=j['description'], requirements=j['requirements'],
            skills_required=j['skills_required'], salary_range=j['salary_range'],
            is_active=True, views=random.randint(10, 500),
            created_at=now - timedelta(days=random.randint(1, 30)),
            deadline=now + timedelta(days=random.randint(7, 60))
        )
        db.session.add(job)
        db.session.flush()
        job_objs.append(job)

    # ── Posts ──────────────────────────────────────────
    print("Creating posts...")
    all_posters = all_users
    for i, p_data in enumerate(POSTS):
        poster = all_posters[i % len(all_posters)]
        post = Post(
            user_id=poster.id, content=p_data['content'], post_type=p_data['type'],
            likes_count=random.randint(5, 280), comments_count=random.randint(1, 40),
            shares_count=random.randint(0, 60),
            created_at=now - timedelta(days=random.randint(1, 60), hours=random.randint(0,23))
        )
        db.session.add(post)
        db.session.flush()
        # Add some likes
        likers = random.sample(all_posters, min(random.randint(3, 12), len(all_posters)))
        for liker in likers:
            if liker.id != poster.id:
                db.session.add(Like(post_id=post.id, user_id=liker.id))

    # Add more posts to reach ~100
    extra_contents = [
        "Just submitted my first open source PR! Small but meaningful. Every contribution counts 🚀 #OpenSource #GitHub",
        "Remember: your network is your net worth. But build it genuinely. Help first, ask later. #Networking",
        "3 am debug session just ended. Found the bug — a missing semicolon. 6 hours. A semicolon. #DevLife",
        "Completed AWS Solutions Architect certification! Took 2 months of prep. Worth every hour. ☁️ #AWS #CloudComputing",
        "Interview tip: When you don't know the answer, say 'Let me think through this.' Silence is fine. Pretending isn't. #Interviews",
        "My startup failed after 8 months. Lessons learned: market > product, talk to customers before building, quit earlier. #Failure #Learning",
        "4 resume mistakes costing you interviews: 1) No numbers/metrics, 2) Responsibilities not achievements, 3) Outdated skills at top, 4) Wrong length #Resume",
        "AI is changing tech but not replacing good engineers. It's amplifying output of those who understand systems and communicate clearly. Upskill accordingly. #AI",
        "Today's wins: fixed a production bug affecting 10k users, shipped a feature, reviewed 4 PRs, and still had dinner by 7pm. Good day. 💪",
        "For students: internship > side projects > academics (in terms of resume weight). Fight for the internship. #Internship #CareerAdvice",
        "What they don't teach in college: how to disagree in code reviews, how to give critical feedback, how to fail fast. Soft skills matter enormously.",
        "Gratitude post: A random alumni I connected with on this platform spent 2 hours helping me prep for my Google interview. I got the offer. Pay it forward. 🙏",
        "The gap between junior and senior engineer isn't code quality — it's understanding the WHY behind decisions. Train for that. #SeniorEngineer",
        "Python > Java for ML, Go > Java for distributed systems, JavaScript is everywhere. Pick your tools by problem, not by preference. #Programming",
        "Just hit 1000 connections on LinkedIn. If you're a student reading this: start building your professional presence NOW, not after you graduate. #LinkedIn",
        "We hire for curiosity, not just skills. In every interview, I try to catch a moment where someone forgets they're being interviewed and just geeks out. #Hiring #TechInterviews",
        "Salary negotiation tip: Always negotiate. The worst they say is no. The gap between first offer and final offer at FAANG can be ₹5-15 LPA. Ask. #SalaryNegotiation",
        "My mental health > my productivity. Took a day off last week with zero guilt. Came back sharper. Normalize rest. #MentalHealth #TechLife",
        "Building in public is underrated. Tweet/post your projects as you build them. Gets you: feedback, followers, accountability, and sometimes, job offers.",
        "To all first-gen tech students: you belong here. The industry needs your perspective. Your background is a strength, not a deficit. Keep going. 💙",
    ]
    for i, content in enumerate(extra_contents):
        poster = all_posters[i % len(all_posters)]
        post = Post(
            user_id=poster.id, content=content, post_type="text",
            likes_count=random.randint(3, 150), comments_count=random.randint(0, 25),
            created_at=now - timedelta(days=random.randint(1, 90), hours=random.randint(0,23))
        )
        db.session.add(post)

    db.session.commit()

    # ── Mentorship Requests ────────────────────────────
    print("Creating mentorship records...")
    used_pairs = set()
    for i, (s_user, student) in enumerate(student_objs):
        # Each student has 1-2 mentorship requests
        num_requests = random.randint(1, 2)
        for _ in range(num_requests):
            alum_user, alum = random.choice(alumni_objs)
            if (student.id, alum.id) in used_pairs:
                continue
            used_pairs.add((student.id, alum.id))
            statuses = ["pending"] * 5 + ["accepted"] * 8 + ["rejected"] * 2
            req = MentorshipRequest(
                student_id=student.id, alumni_id=alum.id,
                status=random.choice(statuses),
                message=f"Hi {alum_user.name}! I'm {s_user.name}, studying {student.department}. I'm deeply interested in {alum.domain} and your journey at {alum.company} is incredibly inspiring. Would love your guidance on breaking into this field. I've been working on {student.skills.split(',')[0] if student.skills else 'relevant skills'} and would love your perspective.",
                created_at=now - timedelta(days=random.randint(1, 45))
            )
            db.session.add(req)

    db.session.commit()

    # ── Referrals ──────────────────────────────────────
    print("Creating referral records...")
    ref_pairs = set()
    for i, (s_user, student) in enumerate(student_objs[:10]):
        alum_user, alum = alumni_objs[i % len(alumni_objs)]
        if (student.id, alum.id) in ref_pairs:
            continue
        ref_pairs.add((student.id, alum.id))
        job = random.choice(job_objs) if job_objs else None
        statuses = ["pending"] * 4 + ["approved"] * 4 + ["rejected"] * 2
        status = random.choice(statuses)
        ref = Referral(
            student_id=student.id, alumni_id=alum.id,
            job_id=job.id if job else None,
            company=alum.company,
            position=job.title if job else "Software Engineer",
            message=f"Hi {alum_user.name}! I'm applying for a role at {alum.company} and your profile really inspired me. I've been building {student.skills.split(',')[0] if student.skills else 'skills'} and believe I'd be a great fit. Could you consider referring me? Happy to share my resume and portfolio.",
            status=status,
            alumni_note="Good profile, forwarding to hiring team." if status == "approved" else ("Not the right fit for current openings." if status == "rejected" else None),
            created_at=now - timedelta(days=random.randint(1, 30))
        )
        db.session.add(ref)

    # ── Job Applications ───────────────────────────────
    print("Creating job applications...")
    app_pairs = set()
    for s_user, student in student_objs:
        for job in random.sample(job_objs, min(random.randint(2, 5), len(job_objs))):
            if (job.id, s_user.id) in app_pairs:
                continue
            app_pairs.add((job.id, s_user.id))
            statuses = ["applied"] * 6 + ["shortlisted"] * 2 + ["rejected"] * 2
            app = JobApplication(
                job_id=job.id, user_id=s_user.id,
                status=random.choice(statuses),
                cover_letter=f"I am excited to apply for the {job.title} position at {job.company}. With my background in {student.skills.split(',')[0] if student.skills else 'relevant technologies'} and passion for {student.interests.split(',')[0] if student.interests else 'the industry'}, I believe I would be a strong contributor to your team.",
                created_at=now - timedelta(days=random.randint(1, 20))
            )
            db.session.add(app)

    # ── Knowledge Base ─────────────────────────────────
    print("Creating knowledge base entries...")
    for i, entry_data in enumerate(KNOWLEDGE_ENTRIES):
        author_user, _ = alumni_objs[i % len(alumni_objs)]
        entry = KnowledgeEntry(
            author_id=author_user.id,
            title=entry_data['title'],
            category=entry_data['category'],
            content=entry_data['content'],
            company=entry_data.get('company'),
            role=entry_data.get('role'),
            tags=entry_data.get('tags'),
            is_approved=True,
            views=random.randint(50, 500),
            helpful_count=random.randint(10, 100),
            created_at=now - timedelta(days=random.randint(5, 60))
        )
        db.session.add(entry)

    # ── Follow relationships ───────────────────────────
    print("Creating follow relationships...")
    follow_pairs = set()
    for s_user, _ in student_objs:
        for a_user, _ in random.sample(alumni_objs, min(3, len(alumni_objs))):
            if (s_user.id, a_user.id) not in follow_pairs:
                follow_pairs.add((s_user.id, a_user.id))
                db.session.add(Follow(follower_id=s_user.id, following_id=a_user.id,
                                      created_at=now - timedelta(days=random.randint(1,60))))

    # ── Notifications ──────────────────────────────────
    print("Creating sample notifications...")
    for s_user, student in student_objs[:5]:
        a_user, alum = random.choice(alumni_objs)
        db.session.add(Notification(
            user_id=s_user.id, type="mentor_accept",
            title="Mentorship Request Accepted! ✅",
            message=f"{a_user.name} accepted your mentorship request. You can now reach out directly.",
            link="/student/mentorship", is_read=False,
            created_at=now - timedelta(hours=random.randint(1, 48))
        ))

    db.session.commit()
    print("\n✅ Seed complete!")
    print("─" * 50)
    print(f"  👑 Admin:    admin@demo.com / Demo@1234")
    print(f"  🎓 Student:  student@demo.com / Demo@1234")
    print(f"  🌟 Alumni:   alumni@demo.com / Demo@1234")
    print("─" * 50)
    print(f"  Students:   {len(STUDENTS)}")
    print(f"  Alumni:     {len(ALUMNI)}")
    print(f"  Companies:  {len(COMPANIES)}")
    print(f"  Jobs:       {len(JOBS_DATA)}")
    print(f"  Posts:      {len(POSTS) + len(extra_contents)}")
    print(f"  Communities:{len(COMMUNITIES)}")
    print(f"  Knowledge:  {len(KNOWLEDGE_ENTRIES)}")
    print("─" * 50)


if __name__ == "__main__":
    with app.app_context():
        seed_all()
