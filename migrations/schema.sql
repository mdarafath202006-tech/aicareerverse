-- ============================================================
--  AI CareerVerse – Full MySQL Schema
--  Run: mysql -u root -p < schema.sql
-- ============================================================

CREATE DATABASE IF NOT EXISTS aicareerverse
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE aicareerverse;

-- ── Users ──────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    name             VARCHAR(100) NOT NULL,
    email            VARCHAR(150) UNIQUE NOT NULL,
    password         VARCHAR(256) NOT NULL,
    role             ENUM('student','alumni','admin') DEFAULT 'student',
    is_active        BOOLEAN DEFAULT TRUE,
    email_verified   BOOLEAN DEFAULT FALSE,
    avatar_url       VARCHAR(500),
    cover_url        VARCHAR(500),
    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email),
    INDEX idx_role  (role)
);

-- ── Students ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL UNIQUE,
    department      VARCHAR(100),
    year            VARCHAR(10),
    skills          TEXT,
    interests       TEXT,
    bio             TEXT,
    github_url      VARCHAR(255),
    linkedin_url    VARCHAR(255),
    resume_url      VARCHAR(500),
    ai_score        INT DEFAULT 0,
    placement_score INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FULLTEXT idx_skills (skills, interests)
);

-- ── Alumni ─────────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS alumni (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL UNIQUE,
    graduation_year YEAR,
    company         VARCHAR(150),
    job_role        VARCHAR(150),
    skills          TEXT,
    location        VARCHAR(100),
    linkedin        VARCHAR(255),
    github_url      VARCHAR(255),
    bio             TEXT,
    rating          DECIMAL(3,2) DEFAULT NULL,
    mentorship_score INT DEFAULT 0,
    impact_score     INT DEFAULT 0,
    is_hiring        BOOLEAN DEFAULT FALSE,
    mentorship_slots INT DEFAULT 3,
    domain           VARCHAR(100),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FULLTEXT idx_skills (skills, bio),
    INDEX idx_company  (company),
    INDEX idx_job_role (job_role)
);

-- ── Mentorship Requests ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS mentorship_requests (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    student_id  INT NOT NULL,
    alumni_id   INT NOT NULL,
    message     TEXT,
    status      ENUM('pending','accepted','rejected') DEFAULT 'pending',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (alumni_id)  REFERENCES alumni(id)   ON DELETE CASCADE,
    UNIQUE KEY uq_request (student_id, alumni_id),
    INDEX idx_alumni_id  (alumni_id),
    INDEX idx_student_id (student_id),
    INDEX idx_status     (status)
);

-- ── Social Posts ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS posts (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    content     TEXT NOT NULL,
    image_url   VARCHAR(500),
    post_type   ENUM('text','image','video','achievement','job') DEFAULT 'text',
    tags        VARCHAR(500),
    likes_count INT DEFAULT 0,
    comments_count INT DEFAULT 0,
    shares_count   INT DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id  (user_id),
    INDEX idx_created  (created_at),
    FULLTEXT idx_content (content)
);

-- ── Post Likes ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS post_likes (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    post_id  INT NOT NULL,
    user_id  INT NOT NULL,
    UNIQUE KEY uq_like (post_id, user_id),
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Post Comments ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS post_comments (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    post_id    INT NOT NULL,
    user_id    INT NOT NULL,
    content    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Stories ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS stories (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    media_url   VARCHAR(500) NOT NULL,
    media_type  ENUM('image','video') DEFAULT 'image',
    caption     VARCHAR(500),
    views_count INT DEFAULT 0,
    expires_at  TIMESTAMP NOT NULL,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Communities ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS communities (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(150) NOT NULL,
    description TEXT,
    icon        VARCHAR(10) DEFAULT '👥',
    color       VARCHAR(20) DEFAULT '#6366f1',
    member_count INT DEFAULT 0,
    created_by  INT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- ── Community Members ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS community_members (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    community_id INT NOT NULL,
    user_id      INT NOT NULL,
    role         ENUM('member','moderator','admin') DEFAULT 'member',
    joined_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_membership (community_id, user_id),
    FOREIGN KEY (community_id) REFERENCES communities(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)      REFERENCES users(id)       ON DELETE CASCADE
);

-- ── Jobs & Internships ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS jobs (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    posted_by    INT NOT NULL,
    title        VARCHAR(200) NOT NULL,
    company      VARCHAR(150),
    location     VARCHAR(150),
    job_type     ENUM('full-time','internship','remote','contract') DEFAULT 'full-time',
    skills_req   TEXT,
    description  TEXT,
    salary_range VARCHAR(100),
    apply_url    VARCHAR(500),
    is_active    BOOLEAN DEFAULT TRUE,
    views_count  INT DEFAULT 0,
    apps_count   INT DEFAULT 0,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at   TIMESTAMP,
    FOREIGN KEY (posted_by) REFERENCES users(id) ON DELETE CASCADE,
    FULLTEXT idx_job (title, skills_req, description)
);

-- ── Job Applications ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS job_applications (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    job_id     INT NOT NULL,
    student_id INT NOT NULL,
    resume_url VARCHAR(500),
    status     ENUM('applied','shortlisted','rejected','hired') DEFAULT 'applied',
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_application (job_id, student_id),
    FOREIGN KEY (job_id)     REFERENCES jobs(id)     ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- ── Notifications ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL,
    type        VARCHAR(50),
    title       VARCHAR(200),
    message     TEXT,
    link        VARCHAR(500),
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_unread (user_id, is_read)
);

-- ── Gamification Points ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_points (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    user_id     INT NOT NULL UNIQUE,
    total_pts   INT DEFAULT 0,
    mentor_pts  INT DEFAULT 0,
    post_pts    INT DEFAULT 0,
    job_pts     INT DEFAULT 0,
    help_pts    INT DEFAULT 0,
    updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── User Badges ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS user_badges (
    id        INT AUTO_INCREMENT PRIMARY KEY,
    user_id   INT NOT NULL,
    badge     VARCHAR(100),
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Chat Messages ──────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS chat_messages (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    room_id     VARCHAR(100) NOT NULL,
    sender_id   INT NOT NULL,
    message     TEXT NOT NULL,
    msg_type    ENUM('text','image','file','voice') DEFAULT 'text',
    is_read     BOOLEAN DEFAULT FALSE,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_room (room_id),
    INDEX idx_sender (sender_id)
);

-- ── Projects Showcase ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS projects (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    title        VARCHAR(200) NOT NULL,
    description  TEXT,
    tech_stack   VARCHAR(500),
    github_url   VARCHAR(500),
    live_url     VARCHAR(500),
    image_url    VARCHAR(500),
    stars_count  INT DEFAULT 0,
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Password Reset Tokens ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS password_reset_tokens (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT NOT NULL,
    token      VARCHAR(128) NOT NULL UNIQUE,
    expires_at TIMESTAMP NOT NULL,
    used       BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- ── Seed Communities ──────────────────────────────────────────────────────
INSERT IGNORE INTO communities (name, description, icon, color, member_count) VALUES
('AI & Machine Learning', 'Discuss AI, ML, deep learning and research', '🤖', '#6366f1', 234),
('Web Development', 'Frontend, backend, full stack discussions', '💻', '#06b6d4', 189),
('Cybersecurity', 'Security, ethical hacking, CTFs', '🔒', '#ef4444', 97),
('Startups & Entrepreneurship', 'Founders, ideas, funding', '🚀', '#f59e0b', 98),
('Competitive Programming', 'Algorithms, DSA, LeetCode, Codeforces', '⚡', '#10b981', 156),
('UI/UX Design', 'Design systems, Figma, user research', '🎨', '#ec4899', 112),
('DevOps & Cloud', 'Docker, K8s, AWS, CI/CD pipelines', '☁️', '#8b5cf6', 88),
('Data Science', 'Analytics, visualization, statistics', '📊', '#f97316', 143);

-- ── Admin user (password: Admin@123) ──────────────────────────────────────
INSERT IGNORE INTO users (name, email, password, role, is_active, email_verified) VALUES
('Admin', 'admin@aicareerverse.com',
 '$2b$12$K9pJN7lNfH4e5x6wD7q8Y.eJcT4v9uRK1HfPzYVoM2L3nX6qS0u3e',
 'admin', TRUE, TRUE);
