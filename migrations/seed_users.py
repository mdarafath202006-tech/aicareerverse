"""
AI CareerVerse – Seed Script
Generates bcrypt-hashed demo users for development.
Run: python migrations/seed_users.py
"""
import mysql.connector
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv
load_dotenv()

CONN = dict(
    host=os.getenv("MYSQL_HOST", "localhost"),
    user=os.getenv("MYSQL_USER", "root"),
    password=os.getenv("MYSQL_PASSWORD", ""),
    database=os.getenv("MYSQL_DB", "aicareerverse"),
    port=int(os.getenv("MYSQL_PORT", 3306)),
)

ALUMNI = [
    ("Arjun Sharma",   "arjun@gmail.com",   "Google",       "Senior Software Engineer",    "Python, Go, System Design, Kubernetes, LeetCode, DSA", "Bangalore",  2020),
    ("Priya Nair",     "priya@gmail.com",   "Amazon",       "Data Scientist",              "Python, ML, TensorFlow, SQL, Statistics, Pandas",       "Hyderabad",  2019),
    ("Vikram Rajan",   "vikram@gmail.com",  "Microsoft",    "ML Engineer",                 "Python, PyTorch, NLP, BERT, Azure, MLOps",              "Pune",       2021),
    ("Deepa Menon",    "deepa@gmail.com",   "Flipkart",     "Frontend Engineer",           "React, TypeScript, Next.js, Redux, CSS, Performance",   "Bangalore",  2022),
    ("Karthik Kumar",  "karthik@gmail.com", "Zomato",       "Backend Engineer",            "Node.js, MongoDB, Redis, AWS, Docker, Microservices",   "Delhi",      2021),
    ("Sneha Reddy",    "sneha@gmail.com",   "Razorpay",     "DevOps Engineer",             "AWS, Kubernetes, Terraform, Jenkins, Linux, CI/CD",     "Hyderabad",  2020),
    ("Rahul Verma",    "rahul@gmail.com",   "Swiggy",       "Product Manager",             "Product Strategy, SQL, Analytics, A/B Testing, Figma",  "Bangalore",  2018),
    ("Divya Krishnan", "divya@gmail.com",   "PhonePe",      "Cybersecurity Analyst",       "Ethical Hacking, Penetration Testing, OWASP, Python",   "Bangalore",  2021),
]

STUDENTS = [
    ("Arun Kumar",     "arun@student.com",   "CSE", "3rd Year", "Python, Java, React, SQL",          "AI/ML, Web Development"),
    ("Meera Patel",    "meera@student.com",  "IT",  "2nd Year", "Python, HTML, CSS, JavaScript",      "Web Development, UX Design"),
    ("Sanjay Singh",   "sanjay@student.com", "CSE", "4th Year", "Python, TensorFlow, Pandas, scikit-learn", "Machine Learning, Data Science"),
    ("Kavya Nair",     "kavya@student.com",  "ECE", "3rd Year", "C++, Python, Arduino",              "IoT, Embedded Systems"),
    ("Rohit Sharma",   "rohit@student.com",  "CSE", "2nd Year", "Java, Spring Boot, MySQL",           "Backend Development"),
]

def seed():
    db  = mysql.connector.connect(**CONN)
    cur = db.cursor()
    pwd = generate_password_hash("Pass@1234")

    print("Seeding alumni...")
    for name, email, company, role, skills, location, grad_year in ALUMNI:
        cur.execute(
            "INSERT IGNORE INTO users (name,email,password,role,is_active,email_verified) VALUES (%s,%s,%s,'alumni',1,1)",
            (name, email, pwd)
        )
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        uid = cur.fetchone()
        if uid:
            cur.execute(
                """INSERT IGNORE INTO alumni
                   (user_id,company,job_role,skills,location,graduation_year,
                    bio,mentorship_score,impact_score,mentorship_slots)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (uid[0], company, role, skills, location, grad_year,
                 f"Experienced {role} at {company} with expertise in {skills.split(',')[0].strip()}. "
                 f"Passionate about mentoring the next generation of engineers.",
                 80, 75, 3)
            )
        print(f"  ✓ {name} ({role} @ {company})")

    print("Seeding students...")
    for name, email, dept, year, skills, interests in STUDENTS:
        cur.execute(
            "INSERT IGNORE INTO users (name,email,password,role,is_active,email_verified) VALUES (%s,%s,%s,'student',1,1)",
            (name, email, pwd)
        )
        cur.execute("SELECT id FROM users WHERE email=%s", (email,))
        uid = cur.fetchone()
        if uid:
            cur.execute(
                "INSERT IGNORE INTO students (user_id,department,year,skills,interests,bio,ai_score) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                (uid[0], dept, year, skills, interests,
                 f"A motivated {year} {dept} student passionate about {interests.split(',')[0].strip()}.",
                 65)
            )
        print(f"  ✓ {name} ({dept} {year})")

    db.commit()
    cur.close(); db.close()
    print("\n✅ Seeding complete! All passwords: Pass@1234")

if __name__ == "__main__":
    seed()
