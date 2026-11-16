# FelixForge Academy — Full-stack starter

A Flask-based programming-learning platform with real accounts, a relational database, a multi-file editor, saved projects, lesson progress, quiz-result storage, an optional AI tutor and an opt-in isolated code runner.

## 1. Requirements

- Windows 11, macOS or Linux
- Python 3.11 or newer
- A modern browser
- Optional: Docker Desktop (only if you want to test the server-side code runner)

## 2. Run locally on Windows 11

Open PowerShell in this folder and run:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env` and replace `SECRET_KEY` with a long random secret. You can generate one with:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

Copy the output into `.env`. Keep `.env` private and never upload it to GitHub.

Start the website:

```powershell
python app.py
```

Open **http://127.0.0.1:5000** in your browser. Create an account. The SQLite database (`codecraft.db`) is created automatically and the learning paths are seeded on first run. Keep this database file when updating a local installation; it contains user accounts and learning progress.

## 3. What's included

- User signup/login/logout with server-side password hashing (Werkzeug scrypt)
- Remember-me sign-in for up to 30 days, provided the app secret and persistent database remain unchanged
- Daily learner activity tracking and an administrator dashboard with learner, activity, lesson, quiz and project metrics
- Learner suggestions and bug reports with administrator status updates and responses
- CSRF protection on forms and JSON API requests
- SQLite by default; configurable SQLAlchemy database URL
- 16 programming learning paths with expanded language-specific lessons, worked examples and practice prompts
- Per-account lesson progress, five interactive mini-quizzes and quiz-result tracking
- Multi-file editor with CodeMirror syntax highlighting, tabs, file explorer and saved projects
- Browser preview for HTML/CSS and sandboxed JavaScript preview
- Optional AI tutor through an OpenAI-compatible chat-completions endpoint
- Optional Docker-based execution for Python, JavaScript, C, C++, Java, PHP, Ruby and Go

The editor's HTML/CSS/JavaScript preview is a learning convenience, not a full browser IDE. Server execution is not enabled by default. SQL, TypeScript and other editor languages can be written and saved, but do not have a server runner configured in this starter.

## 4. Optional AI tutor

The AI tutor is disabled until you configure a provider. Add these settings to `.env`:

```dotenv
AI_API_URL=https://YOUR_PROVIDER_HOST/v1/chat/completions
AI_API_KEY=your_private_api_key
AI_MODEL=your-provider-model-name
```

Use the endpoint, model name and API-key format documented by your chosen provider. Keep the key only in the server's `.env`; do not put it in `static/`, templates or browser JavaScript. Requests send the learner's question and the current editor file to the configured provider. Tell learners not to paste secrets or private data into the tutor.

## 5. Optional Docker code runner — read before enabling

**Do not enable this on a public website or a shared production server as-is.** Running untrusted programs is a high-risk service. A container reduces risk but is not a perfect security boundary. The app launches Docker with no network, a read-only workspace, memory/CPU/PID limits, dropped Linux capabilities, a non-root user and an 8-second timeout. A Docker daemon socket is highly privileged; giving a web process access to it can effectively grant control over the host.

For local experiments only:

1. Install Docker Desktop and start it.
2. Confirm `docker run --rm hello-world` works from the same terminal that will run Flask.
3. Pull the required runtime images before testing, e.g. `docker pull python:3.12-alpine`, `docker pull node:22-alpine`, `docker pull gcc:14`, `docker pull eclipse-temurin:21-jdk`, `docker pull php:8.3-cli-alpine`, `docker pull ruby:3.3-alpine`, and `docker pull golang:1.23-alpine`.
4. Set `ENABLE_CODE_RUNNER=true` in `.env` and restart Flask.
5. Test only with harmless sample programs and keep the service bound to localhost.

For a real public service, move code execution into a separate, disposable worker/VM or dedicated sandbox service. Do not mount the host Docker socket into a public web container. Add authentication, per-user quotas, rate limiting, queue limits, logging, abuse monitoring, network isolation, seccomp/AppArmor or stronger sandboxing, and an administrator kill switch. Have the isolation design reviewed by a security professional before accepting untrusted code.

## 6. Persistent accounts, sign-in and learner progress

The app now uses a 30-day remember-me cookie. Users should not need to sign in again after an ordinary server restart or code-only update, as long as the same `SECRET_KEY` is kept and the browser still has its remember cookie. Do not regenerate `SECRET_KEY` for every deployment. If it changes, existing signed sessions and remember cookies become invalid.

Learner progress, bookmarks, notes, projects and quiz results are stored in the database, not in the code files. Keep the database on durable storage. For a public deployment, use a managed PostgreSQL database and keep the same `DATABASE_URL` across releases. Do not delete or replace the database when uploading a new ZIP or redeploying. The updated lesson seeding logic keeps existing lesson IDs and appends new lessons so existing progress remains attached to the correct lesson records. For a local ZIP update, extract the new code over the existing project folder or copy the old `codecraft.db` into the updated folder before starting the app; the ZIP intentionally does not include a live user database.

The new activity and suggestions features create additional database tables automatically with `db.create_all()`. The administrator account is provisioned from the private `ADMIN_EMAIL`, `ADMIN_USERNAME` and `ADMIN_PASSWORD` settings; admin access stays disabled unless both email and password are configured. There is no hard-coded default admin password. That creates missing tables, but it is not a general-purpose schema migration system. Back up the database before upgrades and use Flask-Migrate/Alembic for future structural schema changes.

## 7. Administrator account and learner suggestions

1. Set `ADMIN_EMAIL`, `ADMIN_USERNAME` and a strong `ADMIN_PASSWORD` (at least 16 characters) in the private environment variables or local `.env` file. Never commit these values to GitHub.
2. On startup, the app creates the administrator account if it does not already exist. It hashes the password before storing it. The configured administrator password remains authoritative and is applied to the admin account at startup, so rotating the environment variable changes the admin login password.
3. Sign in using the configured email and password, then open `/admin`. Public sign-up cannot claim the configured administrator email address.
4. The dashboard shows registered learners, active learners in the last seven days, new learners in the last 30 days, course and lesson totals, lesson completions, quiz attempts, project submissions, discussions and suggestions.
5. Learners can submit ideas and bug reports from the Suggestions tab. The administrator can update each suggestion's status and send a response.

Activity statistics count signed-in accounts once per day. They are not a count of anonymous visitors or a real-time analytics tracker.

## 8. Database and deployment notes

- SQLite is suitable for local learning and a small single-instance demo.
- For a deployed multi-user service, use PostgreSQL and a managed database. Install a PostgreSQL driver such as `psycopg[binary]`, then set `DATABASE_URL` to your provider's connection URL.
- `db.create_all()` creates missing tables but does not migrate existing schemas. Use Alembic/Flask-Migrate before making schema changes in a live deployment.
- Set a strong `SECRET_KEY`, `COOKIE_SECURE=true` behind HTTPS, `FLASK_DEBUG` off, and configure backups, logging and monitoring.
- Use a production WSGI server such as Gunicorn (Linux) or Waitress (Windows); do not run Flask's development server as a public production service.
- Add email verification, password reset, rate limiting, account deletion/export, privacy notice and terms before public launch.
- The AI tutor needs provider billing/usage limits and moderation appropriate to your audience.

## 9. Deploy to Railway (public website)

1. Push this project to a **private GitHub repository**. Do not commit `.env`, API keys, database files or passwords.
2. In Railway, create a project and choose **Deploy from GitHub repo**. Select this repository.
3. Add a PostgreSQL service to the Railway project. Ensure the web service receives the database connection as `DATABASE_URL` (Railway commonly offers a reference variable such as `${{Postgres.DATABASE_URL}}`).
4. Add a `SECRET_KEY` service variable containing a newly generated random value of at least 32 characters. Generate one locally with `python -c "import secrets; print(secrets.token_urlsafe(48))"`. Do not paste it into source code or commit it.
5. Set `FLASK_ENV=production`, `ADMIN_EMAIL`, `ADMIN_USERNAME`, and a strong `ADMIN_PASSWORD` (at least 16 characters), and set `ENABLE_CODE_RUNNER=false`. Keep `SECRET_KEY` and the PostgreSQL `DATABASE_URL` unchanged across future deployments. The app automatically enables secure session cookies in production.
6. Deploy, wait for the health check, then use Railway's generated public domain. Test signup, logout/login, creating a project, saving it and lesson progress.
7. Configure database backups and a custom domain only after the generated domain passes testing.

**Important:** The public code runner intentionally remains disabled. Do not enable it on the web service; public code execution needs a separate hardened sandbox service. Configure AI provider secrets in Railway's Variables page only if you have an API provider and have reviewed its privacy and usage terms.

## 8. Important limitations

This is a full-stack learning platform starter, not a finished commercial SaaS. Email verification, password reset, billing, cloud file storage, anonymous visitor analytics and a production-grade execution cluster still need separate implementation or configuration. Cross-device progress depends on all app instances using the same durable database. The included lessons are introductory seed content and should be expanded and reviewed before teaching at scale.

## Curriculum content
The core lesson curriculum is maintained in `curriculum.py`; additional language-specific lessons are in `additional_curriculum.py`; and the beginner-first sequence is maintained in `beginner_curriculum.py`. The platform now seeds 331 lessons across 16 learning paths, including 135 new beginner foundation lessons. Each programming-language path starts with a first program, variables and data types, operators, decisions, loops, functions, collections, structured data/objects, and input/output with basic validation. HTML, CSS and SQL have matching subject-specific foundations. Lessons include learning objectives, plain-language explanations, worked examples, common mistakes and practice tasks. On startup, the seed routine matches lessons by title and updates their order while retaining existing lesson IDs, so saved progress, notes and bookmarks remain attached to the same lessons. Older custom lessons are retained after the maintained curriculum.


## Curriculum practice and copyright

FelixForge Academy includes course-specific guided coding exercises, portfolio project briefs, and a 10-question end-of-course assessment for every learning path. Exercises include requirements, implementation guidance, and test criteria. Project briefs include functional requirements and a suggested build process.

Copyright: © 2026 Felix Saviour Oluebubechukwu. All rights reserved. FelixForge Academy is an educational project.

### Expanded worked examples
Every lesson now includes its original main example plus two additional language-specific worked examples. Each added example has a short explanation and is displayed directly on the lesson page. The examples cover all 16 learning paths.

## Expanded learning experience (November 2026)

The lesson experience now includes:
- A beginner-first curriculum of 331 lessons across all 16 learning paths, including 135 new foundations lessons with worked examples.
- A main worked example plus three additional language-specific worked examples per lesson where the course has supporting examples.
- Expected-behaviour notes and a line-by-line code reading guide for each displayed example.
- Topic checklists, common mistakes, independent challenges and personal lesson notes.
- Lesson bookmarks, global course/lesson search, a compact layout and a saved light/dark theme preference.
- A 15-minute, shuffled course assessment experience with feedback after submission.
- Learning streaks, achievement milestones and printable completion certificates (all lessons plus at least 80% on an assessment).
- A student discussion board, replies, in-app notifications and administrator announcements.
- A learner project portfolio and project submission descriptions/links.
- An administrator overview and lesson editor protected by the `ADMIN_EMAIL` setting.

### Optional administrator account

Set `ADMIN_EMAIL` in the environment to the email address of the administrator account. The admin dashboard is available at `/admin`. Do not expose this setting publicly or give administrator access to an untrusted account.

### Code execution and AI tutor

The code runner remains disabled unless `ENABLE_CODE_RUNNER=true` is configured and Docker is available. The runner is designed to use isolated containers with no network access and resource limits. Review the deployment and container configuration before enabling execution on a public server. Do not run untrusted code directly in the Flask process.

The AI tutor requires a compatible provider endpoint and credentials configured with `AI_API_URL`, `AI_API_KEY` and `AI_MODEL`. Keep API keys on the server; never place them in browser JavaScript or commit them to GitHub.

### Features that need additional service integration

Email verification, password-reset email delivery, GitHub OAuth, real-time push notifications, hosted collaborative study rooms, live coding competitions, peer-review workflows, and automated email reports need additional provider configuration and moderation/operational work. The in-app discussion board, project portfolio, announcements and notification inbox are available without those external services. The discussion board is a basic community feature; add active moderation, reporting and clear community rules before opening it to a large public audience.

### Database note

New tables are created by the existing `db.create_all()` startup step. Existing lesson records are updated by course position so saved progress continues to point to the same lesson IDs. Back up your database before replacing files on a live installation.

## Membership pricing and administrator reporting

- Free learning plan: ₦0.
- Monthly membership: ₦5,000 for 30 days.
- Annual membership: ₦50,000 for 365 days (₦10,000 less than twelve monthly payments).
- Membership payments are one-time transactions for a fixed access period; automatic recurring billing is not enabled.
- Course certificates remain separate at the configured one-time per-course fee (`CERTIFICATE_FEE_NAIRA`, default ₦2,000).
- Set `MEMBERSHIP_MONTHLY_NAIRA=5000` and `MEMBERSHIP_ANNUAL_NAIRA=50000` in private environment variables to use these prices. Successful Paystack transactions are verified server-side before membership access dates are recorded.
- The admin dashboard includes recent individual quiz attempts, learner plan/payment history, active free/paid plan counts, and membership revenue.

Before enabling real payments, the platform owner should clearly publish the specific benefits included in paid membership and have a parent/guardian assist with payment-provider accounts and financial obligations where required.

## FelixForge Academy Premium Advanced Courses

The Advanced Courses library contains 11 specialist tracks covering advanced Python, Flask full-stack development, JavaScript, React, database engineering, data structures and algorithms, API engineering, cloud/DevOps, secure web development, machine learning and software testing/CI. Each track is seeded with lesson explanations, code examples, practice work and a short assessment.

Advanced lesson content is protected on the server. A learner needs a verified, currently active monthly or annual membership; the configured administrator is allowed through without a paid membership. Free and expired learners can preview course descriptions and see the membership prompt, but protected lesson, practice, quiz and lesson-action endpoints check access independently. Keep the same database when updating so existing accounts and progress are retained.

The public-facing platform name is **FelixForge Academy**. Its main motto is **From Zero to Developer**, with the supporting line **Learn coding at your own pace**. The landing page also retains **Turn curiosity into real-world code** and **Your next chapter starts here**.
