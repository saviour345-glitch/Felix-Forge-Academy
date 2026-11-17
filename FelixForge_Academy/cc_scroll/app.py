import os, json, uuid, tempfile, subprocess, pathlib, textwrap, urllib.request, urllib.error
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, session
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = pathlib.Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')
app = Flask(__name__)
IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production' or bool(os.environ.get('RAILWAY_ENVIRONMENT'))
secret_key = os.environ.get('SECRET_KEY', '')
if IS_PRODUCTION and len(secret_key) < 32:
    raise RuntimeError('Set SECRET_KEY to a random value of at least 32 characters before deployment.')
app.config['SECRET_KEY'] = secret_key or 'dev-only-change-this-secret-before-deployment'
app.config['ADMIN_EMAIL'] = os.environ.get('ADMIN_EMAIL', '').strip().lower()
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'admin').strip() or 'admin'
app.config['ADMIN_ENABLED'] = bool(app.config['ADMIN_EMAIL'] and os.environ.get('ADMIN_PASSWORD', ''))
app.config['CERTIFICATE_FEE_NAIRA'] = max(0, int(os.environ.get('CERTIFICATE_FEE_NAIRA', '2000')))
app.config['MEMBERSHIP_MONTHLY_NAIRA'] = max(0, int(os.environ.get('MEMBERSHIP_MONTHLY_NAIRA', '5000')))
app.config['MEMBERSHIP_ANNUAL_NAIRA'] = max(0, int(os.environ.get('MEMBERSHIP_ANNUAL_NAIRA', '50000')))
app.config['PAYSTACK_SECRET_KEY'] = os.environ.get('PAYSTACK_SECRET_KEY', '').strip()
database_url = os.environ.get('DATABASE_URL', f"sqlite:///{BASE_DIR / 'codecraft.db'}")
# Railway may provide postgres://; use the installed psycopg v3 driver explicitly.
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
elif database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
# Persistent sign-in across ordinary browser restarts and app deployments.
# This still depends on keeping SECRET_KEY stable and using durable database storage.
app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION or os.environ.get('COOKIE_SECURE', 'false').lower() == 'true'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SECURE'] = app.config['SESSION_COOKIE_SECURE']
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='owner', cascade='all, delete-orphan')
    progress = db.relationship('Progress', backref='learner', cascade='all, delete-orphan')
    quiz_results = db.relationship('QuizResult', back_populates='learner', cascade='all, delete-orphan')
    def set_password(self, password): self.password_hash = generate_password_hash(password, method='scrypt')
    def check_password(self, password): return check_password_hash(self.password_hash, password)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(40), unique=True, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    level = db.Column(db.String(30), default='Beginner')
    description = db.Column(db.Text, default='')
    language = db.Column(db.String(30), nullable=False)
    access_level = db.Column(db.String(20), nullable=False, default='free')
    lessons = db.relationship('Lesson', backref='course', cascade='all, delete-orphan', order_by='Lesson.position')

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)
    example = db.Column(db.Text, default='')
    position = db.Column(db.Integer, default=1)

class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id'),)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    language = db.Column(db.String(24), nullable=False, default='python')
    files_json = db.Column(db.Text, default='{}')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class QuizQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_slug = db.Column(db.String(40), nullable=False)
    prompt = db.Column(db.String(300), nullable=False)
    options_json = db.Column(db.Text, nullable=False)
    correct_index = db.Column(db.Integer, nullable=False)
    explanation = db.Column(db.String(500), default='')
    position = db.Column(db.Integer, default=1)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_slug = db.Column(db.String(40), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    learner = db.relationship(
        'User',
        back_populates='quiz_results'
    )

class CertificatePayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_slug = db.Column(db.String(40), nullable=False)
    reference = db.Column(db.String(100), unique=True, nullable=False)
    amount_kobo = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    certificate_name = db.Column(db.String(80), nullable=True)
    learner = db.relationship('User', backref=db.backref('certificate_payments', lazy=True))


class MembershipPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plan = db.Column(db.String(20), nullable=False)  # free, monthly, annual
    reference = db.Column(db.String(100), unique=True)
    amount_kobo = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    paid_at = db.Column(db.DateTime)
    starts_at = db.Column(db.DateTime)
    ends_at = db.Column(db.DateTime)
    learner = db.relationship('User', backref=db.backref('membership_payments', lazy=True))

class LessonBookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id'),)

class LessonNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    content = db.Column(db.Text, default='')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'lesson_id'),)

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class CommunityRestriction(db.Model):
    """Administrator-issued restriction from the community area only."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', foreign_keys=[user_id])
    admin = db.relationship('User', foreign_keys=[admin_id])

class CommunityUserBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blocker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    blocked_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    blocked_user = db.relationship('User', foreign_keys=[blocked_id])
    __table_args__ = (db.UniqueConstraint('blocker_id', 'blocked_id'),)

class CommunityReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('forum_reply.id'))
    reason = db.Column(db.String(60), nullable=False)
    details = db.Column(db.String(1000), default='')
    status = db.Column(db.String(20), nullable=False, default='Open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reporter = db.relationship('User', foreign_keys=[reporter_id])
    reported_user = db.relationship('User', foreign_keys=[reported_user_id])

class ProjectSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_slug = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    project_url = db.Column(db.String(500), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.String(1000), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_date = db.Column(db.Date, nullable=False, default=date.today)
    last_seen_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'activity_date'),)

class Suggestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(40), nullable=False, default='General')
    title = db.Column(db.String(140), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='New')
    admin_note = db.Column(db.String(1000), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('User')

@login_manager.user_loader
def load_user(user_id): return db.session.get(User, int(user_id))

COURSE_SEED = [
 ('python','Python','Python','Beginner','Learn variables, conditions, loops, functions and useful standard-library tools.'),
 ('html','HTML','HTML','Beginner','Build accessible page structure with semantic HTML.'),
 ('css','CSS','CSS','Beginner','Style responsive interfaces with layout, typography and modern CSS.'),
 ('javascript','JavaScript','JavaScript','Beginner','Make websites interactive with JavaScript and the DOM.'),
 ('c','C Programming','C','Beginner','Understand procedural programming, types, functions and memory basics.'),
 ('cpp','C++','C++','Beginner','Learn C++ fundamentals, classes and the standard library.'),
 ('java','Java','Java','Beginner','Learn object-oriented programming and Java fundamentals.'),
 ('csharp','C#','C#','Beginner','Build a foundation in C# syntax, types and classes.'),
 ('php','PHP','PHP','Beginner','Learn server-side programming and web fundamentals.'),
 ('sql','SQL','SQL','Beginner','Query relational databases and work with structured data.'),
 ('typescript','TypeScript','TypeScript','Beginner','Add static types to JavaScript projects.'),
 ('go','Go','Go','Beginner','Explore a compiled language designed for simple, reliable software.'),
 ('rust','Rust','Rust','Beginner','Learn ownership, borrowing and safe systems programming.'),
 ('ruby','Ruby','Ruby','Beginner','Learn expressive syntax, methods and collections.'),
 ('swift','Swift','Swift','Beginner','Explore Swift language fundamentals.'),
 ('kotlin','Kotlin','Kotlin','Beginner','Learn modern Kotlin syntax and object-oriented concepts.'),
]
from curriculum import CURRICULUM
from beginner_curriculum import BEGINNER_LESSONS
from worked_examples import extra_examples
from practice_content import PRACTICE
from lesson_tools import code_walkthrough, expected_behaviour
from lesson_enrichment import deep_dive
from additional_curriculum import ADDITIONAL_LESSONS
LESSONS = CURRICULUM
DEFAULT_LESSONS = [('Language overview','This course introduces the language, its purpose, and the tools used to write and run programs. Work through the explanation, inspect the example, then complete the practice task before moving on.','// Start with a small program, run it, and change one thing at a time.')]

def seed_database():
    # Keep lesson IDs stable when updating existing installations so saved progress remains linked.
    for slug,title,language,level,description in COURSE_SEED:
        course = Course.query.filter_by(slug=slug).first()
        if not course:
            course = Course(slug=slug,title=title,language=language,level=level,description=description)
            db.session.add(course)
            db.session.flush()
        else:
            course.title, course.language, course.level, course.description = title, language, level, description
        # Beginner foundations appear first. Match existing lessons by title rather
        # than position so inserting new foundations never changes the lesson IDs
        # that existing progress, notes and bookmarks refer to.
        lesson_data = (
            list(BEGINNER_LESSONS.get(slug, []))
            + list(LESSONS.get(slug, DEFAULT_LESSONS))
            + list(ADDITIONAL_LESSONS.get(slug, []))
        )
        # Remove duplicate titles while preserving the first (beginner-first) order.
        ordered_data = []
        seen_titles = set()
        for lesson_title, body, example in lesson_data:
            if lesson_title in seen_titles:
                continue
            seen_titles.add(lesson_title)
            ordered_data.append((lesson_title, body, example))

        existing_by_title = {}
        for old_lesson in course.lessons:
            existing_by_title.setdefault(old_lesson.title, old_lesson)
        used_ids = set()
        next_position = 1
        for lesson_title, body, example in ordered_data:
            lesson_row = existing_by_title.get(lesson_title)
            if lesson_row is None or lesson_row.id in used_ids:
                lesson_row = Lesson(course_id=course.id, title=lesson_title,
                                    body=body, example=example, position=next_position)
                db.session.add(lesson_row)
            else:
                lesson_row.title = lesson_title
                lesson_row.body = body
                lesson_row.example = example
                lesson_row.position = next_position
                used_ids.add(lesson_row.id)
            next_position += 1

        # Preserve any locally-created/legacy lesson not present in the curriculum
        # by moving it after the maintained lessons instead of deleting it.
        for old_lesson in course.lessons:
            if old_lesson.id not in used_ids and old_lesson.title not in seen_titles:
                old_lesson.position = next_position
                next_position += 1
        # Never delete older lesson rows during a content update: progress, notes,
        # bookmarks and learner references depend on their stable IDs.
    db.session.commit()
    if not QuizQuestion.query.count():
        quiz_seed = {
          'python':[('Which keyword defines a function in Python?',['func','def','function','method'],1,'Python uses def to define a function.'),('Which collection stores ordered, changeable items?',['tuple','set','list','frozenset'],2,'A list is ordered and mutable.'),('What does len([2, 4, 6]) return?',['2','3','6','12'],1,'There are three items in the list.')],
          'html':[('Which element is the main page heading?',['head','h1','title','header'],1,'h1 is the top-level heading element.'),('Which attribute provides image alternative text?',['src','href','alt','title'],2,'alt describes the image for users who cannot see it.'),('Which element creates a hyperlink?',['link','a','href','url'],1,'The a element creates a hyperlink.')],
          'css':[('Which property changes text colour?',['font-style','background','color','text-size'],2,'The color property sets text colour.'),('Which declaration enables Flexbox?',['display: flex','position: flex','flex: display','layout: flex'],0,'display:flex creates a flex formatting context.'),('Which selector targets an element with id menu?',['.menu','#menu','menu','*menu'],1,'An ID selector starts with #.')],
          'javascript':[('Which keyword declares a block-scoped variable that can be reassigned?',['const','let','static','define'],1,'let declares a reassignable block-scoped binding.'),('Which method selects the first matching CSS selector?',['getElementByIdAll','querySelector','selectFirst','findNode'],1,'document.querySelector returns the first match.'),('What does === compare?',['Only types','Only values','Value and type','Object keys'],2,'Strict equality compares without type coercion.')],
          'sql':[('Which SQL command retrieves rows?',['PUSH','SELECT','FETCHALL','OPEN'],1,'SELECT retrieves data from tables or views.'),('Which clause filters rows?',['ORDER BY','GROUP BY','WHERE','JOIN'],2,'WHERE filters rows before grouping.'),('Which keyword sorts results?',['SORT','ORDER BY','ARRANGE','RANK'],1,'ORDER BY sorts query results.')]
        }
        for slug, questions in quiz_seed.items():
            for i,(prompt,options,correct,explanation) in enumerate(questions,1):
                db.session.add(QuizQuestion(course_slug=slug,prompt=prompt,options_json=json.dumps(options),correct_index=correct,explanation=explanation,position=i))
        db.session.commit()

    # Ensure every course has a proper 10-question end-of-course assessment.
    # Existing question IDs and learner results are retained; only missing questions are added.
    universal_exam = [
      ('What is the main purpose of a variable?', ['To store a value for later use','To repeat code automatically','To style a page','To stop a program'], 0, 'A variable gives a name to a value so the program can use or update it.'),
      ('Which structure is used to make a decision?', ['A loop','A conditional statement','A comment','A file'], 1, 'A conditional chooses a path based on whether a condition is true or false.'),
      ('When is a loop most useful?', ['When an operation must be repeated','When naming a file','When declaring a colour','When ending a program'], 0, 'Loops repeat instructions while a condition holds or for each item.'),
      ('What is the main benefit of a function?', ['It makes every value global','It groups reusable instructions under a name','It removes the need to test','It stores data permanently'], 1, 'Functions organise behaviour into reusable units.'),
      ('What should a program do when input is invalid?', ['Crash without explanation','Silently accept it','Validate it and give a useful message','Delete unrelated data'], 2, 'Good programs validate input and explain how to correct invalid values.'),
      ('What is a useful first step when debugging?', ['Rewrite the whole program','Reproduce the problem and inspect relevant values','Delete the error message','Add random code'], 1, 'Reproducing the issue helps isolate its cause.'),
      ('Why divide code into small, well-named functions?', ['To make it harder to understand','To improve organisation, reuse and testing','To avoid documentation','To increase file size'], 1, 'Small units with clear responsibilities are easier to maintain.'),
      ('What is the purpose of testing boundary values?', ['Test only typical inputs','Check behaviour at limits','Make an interface colourful','Avoid validation'], 1, 'Boundary tests check edge values such as zero, empty input and maximum values.'),
      ('Which practice helps protect user-provided text on a webpage?', ['Treat all input as trusted markup','Render it safely as text','Put it into executable code','Remove all labels'], 1, 'Untrusted text should not be interpreted as executable markup.'),
      ('What should a useful project README include?', ['Only the author name','Purpose, setup, usage and limitations','Private passwords','Every dependency source code'], 1, 'A README explains how another developer can understand and run a project.'),
      ('What is an algorithm?', ['A computer brand','A finite sequence of steps for solving a problem','A type of monitor','A programming font'], 1, 'An algorithm is a defined procedure for solving a problem.'),
      ('What does a Boolean value represent?', ['A date','True or false','A paragraph','A file path'], 1, 'Boolean values represent one of two logical states.'),
      ('What is an array or list commonly used for?', ['Storing an ordered collection of values','Encrypting a hard drive','Starting a computer','Styling text'], 0, 'Collections store multiple values under one variable.'),
      ('What is a parameter in a function?', ['A value supplied to the function definition for use','A compiler error','A file extension','A screen size'], 0, 'Parameters allow a function to receive input.'),
      ('What does a return statement usually do?', ['Repeats a loop','Sends a result back to the caller','Deletes a function','Opens a browser'], 1, 'A return statement provides a function result and ends that call.'),
      ('What is a syntax error?', ['A mistake in the language grammar','A slow internet connection','A missing keyboard','A design preference'], 0, 'Syntax errors occur when code does not follow the language rules.'),
      ('What is the purpose of a code comment?', ['To explain code to readers','To execute a second program','To encrypt a variable','To increase CPU speed'], 0, 'Comments provide helpful explanations and are not normally executed.'),
      ('Which is the safest way to store an application secret?', ['Hard-code it in public source code','Commit it to GitHub','Use a protected environment variable or secret store','Display it on the homepage'], 2, 'Secrets should be kept outside source code and protected by deployment settings.'),
      ('Why should software dependencies be updated?', ['To remove all tests','To receive fixes and supported improvements','To make passwords public','To disable backups'], 1, 'Updates can fix bugs and security issues; they should be tested before deployment.'),
      ('What is version control used for?', ['Tracking changes to files over time','Increasing screen brightness','Replacing a database','Creating passwords'], 0, 'Version control records changes and supports collaboration and rollback.'),
      ('What does an HTTP 404 response usually mean?', ['The resource was not found','The request succeeded','The server is permanently powered off','The user is an administrator'], 0, 'A 404 status indicates that the requested resource could not be found.'),
      ('What is an API?', ['A defined way for software systems to communicate','A type of battery','A computer desk','A programming language only'], 0, 'An API defines how one software component can request services or data from another.'),
      ('Why validate data on the server even if the browser validates it?', ['Browser checks can be bypassed','It makes pages colourful','It removes the database','It prevents all bugs'], 0, 'Server-side validation protects the application because clients are not trusted.'),
      ('What is a database table?', ['A structured collection of related records','A physical desk','A browser tab','A source-code comment'], 0, 'Tables organise related data into rows and columns.'),
      ('Which SQL command is used to retrieve data?', ['SELECT','DELETE','DROP','UPDATE'], 0, 'SELECT reads data from tables or views.'),
      ('What is a primary key?', ['A field that uniquely identifies each row','A user password','A CSS selector','A backup cable'], 0, 'A primary key uniquely identifies a record in a table.'),
      ('Why use parameterised database queries?', ['To reduce injection risks','To make queries longer','To expose passwords','To disable indexes'], 0, 'Parameters separate data from SQL instructions.'),
      ('What is authentication?', ['Verifying who a user is','Choosing a page colour','Compressing images','Sorting a list'], 0, 'Authentication verifies a claimed identity.'),
      ('What is authorisation?', ['Determining what an authenticated user may access','Creating a username','Formatting source code','Testing a monitor'], 0, 'Authorisation checks permissions after identity has been established.'),
      ('Why should passwords be hashed with a password-hashing algorithm?', ['To avoid storing plaintext passwords','To make them easy to read','To send them to every user','To remove login checks'], 0, 'A suitable password hash makes stored credentials safer if the database is exposed.'),
      ('What is responsive web design?', ['Layouts that adapt to different screen sizes','A page that never changes','A website without HTML','A fixed-size image'], 0, 'Responsive layouts adapt to phones, tablets and desktop screens.'),
      ('What does semantic HTML provide?', ['Meaningful structure for content','A faster internet connection','Database encryption','A programming compiler'], 0, 'Semantic elements communicate the role of page content.'),
      ('What is the DOM?', ['A structured representation of a webpage','A database password','A network cable','A Python package manager'], 0, 'The Document Object Model represents page elements as objects scripts can inspect and update.'),
      ('What does CSS primarily control?', ['Presentation and layout','Database transactions','Server passwords','Network routing'], 0, 'CSS controls how document content is presented.'),
      ('Why use HTTPS?', ['To protect data in transit with encryption','To guarantee a site has no bugs','To make every user an admin','To replace backups'], 0, 'HTTPS protects the connection between browser and server.'),
      ('What is a unit test?', ['A test of a small piece of code in isolation','A full internet speed test','A design mock-up','A database export'], 0, 'Unit tests check individual functions or components.'),
      ('What is integration testing?', ['Checking that components work together','Checking only font size','Removing dependencies','Changing a username'], 0, 'Integration tests examine interactions between parts of a system.'),
      ('What is the purpose of a backup?', ['To restore data after loss or damage','To make data public','To replace access control','To increase screen resolution'], 0, 'Backups provide a recovery copy if primary data is lost.'),
      ('Why should errors be logged carefully?', ['To help diagnose issues without exposing secrets','To publish user passwords','To hide all failures','To replace tests'], 0, 'Useful logs support diagnosis but must avoid sensitive information.'),
      ('What is a software licence?', ['Terms describing how software may be used and shared','A server IP address','A database row','A keyboard shortcut'], 0, 'Licences define permissions and conditions for using software.'),
      ('What is the purpose of a deployment environment variable?', ['Configure an application without embedding settings in code','Change a monitor cable','Store every user password in public','Delete application logs'], 0, 'Environment variables supply configuration separately from source code.'),
      ('What is a loop condition?', ['An expression that determines whether repetition continues','A file name','A comment style','A database table'], 0, 'The condition controls whether a conditional loop continues.'),
      ('What is an infinite loop?', ['A loop that does not reach its stopping condition','A loop that runs exactly twice','A function with no parameters','A syntax highlighting theme'], 0, 'An infinite loop continues because its exit condition is never met.'),
      ('What is type conversion?', ['Changing a value from one data type to another','Deleting a variable','Renaming a folder','Starting a server'], 0, 'Type conversion changes how a value is represented or interpreted.'),
      ('Why is input length validation useful?', ['It helps enforce limits and reduce unexpected processing','It changes the website logo','It removes authentication','It makes all inputs valid'], 0, 'Length limits help protect application behaviour and resource use.'),
      ('What is a merge conflict in version control?', ['Competing changes that need to be reconciled','A failed login','A broken monitor','A database password'], 0, 'A merge conflict occurs when changes overlap and cannot be combined automatically.'),
      ('What should you do before making a risky production change?', ['Back up and test the change in a safe environment','Delete the backup','Disable monitoring','Share administrator credentials'], 0, 'Backups and staging tests reduce the impact of mistakes.'),
      ('What is accessibility in web development?', ['Making content usable by people with different abilities','Making every page identical','Removing all headings','Using only images for text'], 0, 'Accessible design supports a wider range of users and assistive technologies.'),
      ('What is the purpose of pagination?', ['Dividing a large result set into manageable pages','Encrypting a password','Changing code indentation','Deleting old records'], 0, 'Pagination reduces the amount of data shown or loaded at once.'),
      ('Why should an application use least privilege?', ['Give each account only the access needed for its role','Give every user administrator access','Disable all passwords','Share one account'], 0, 'Least privilege limits damage from mistakes or compromised accounts.'),
      ('What is a webhook?', ['An HTTP notification sent when an event occurs','A CSS animation','A local variable','A type of database index'], 0, 'Webhooks notify another service about events, often through an HTTP request.'),
    ]
    universal_exam = universal_exam[:50]
    for course in Course.query.all():
        existing_count = QuizQuestion.query.filter_by(course_slug=course.slug).count()
        if existing_count < 50:
            for pos, (prompt, options, correct, explanation) in enumerate(universal_exam, 1):
                if pos <= existing_count:
                    continue
                db.session.add(QuizQuestion(course_slug=course.slug, prompt=prompt, options_json=json.dumps(options), correct_index=correct, explanation=explanation, position=pos))
    db.session.commit()

# Premium-only advanced curriculum. Existing courses remain free.
ADVANCED_COURSE_SEED = [
    ('advanced-python', 'Advanced Python Engineering', 'Python', 'Advanced',
     'Move beyond syntax into object-oriented design, iterators, decorators, asynchronous programming, testing and packaging.'),
    ('flask-full-stack', 'Full-Stack Development with Flask', 'Python', 'Advanced',
     'Build production-minded Flask applications with authentication, SQLAlchemy, APIs, validation, deployment and security.'),
    ('advanced-javascript', 'Advanced JavaScript Development', 'JavaScript', 'Advanced',
     'Master asynchronous JavaScript, modules, browser APIs, robust application structure and testing.'),
    ('database-engineering', 'Database Design and Engineering', 'SQL', 'Advanced',
     'Design relational databases, use transactions and indexes, write efficient queries and protect data integrity.'),
    ('data-structures-algorithms', 'Data Structures and Algorithms', 'Python', 'Advanced',
     'Study complexity, recursion, searching, sorting, linked structures, stacks, queues, trees and graphs.'),
    ('react-frontend-architecture', 'React and Frontend Architecture', 'JavaScript', 'Advanced',
     'Design reusable React components, manage state, build accessible interfaces and structure maintainable frontend applications.'),
    ('api-engineering', 'Professional API Engineering with Flask', 'Python', 'Advanced',
     'Build reliable APIs with validation, pagination, authentication, consistent errors, testing and API documentation.'),
    ('cloud-devops-engineering', 'Cloud Deployment and DevOps Engineering', 'DevOps', 'Advanced',
     'Understand deployment pipelines, environment configuration, containers, observability, releases and operational reliability.'),
    ('secure-web-engineering', 'Secure Web Application Engineering', 'Security', 'Advanced',
     'Apply defensive web-development practices including input validation, access control, secure sessions, secrets handling and safe file processing.'),
    ('machine-learning-python', 'Machine Learning with Python', 'Python', 'Advanced',
     'Explore data preparation, model training, evaluation, overfitting, pipelines and responsible use of machine-learning systems.'),
    ('software-testing-cicd', 'Software Testing and CI/CD', 'Python', 'Advanced',
     'Build confidence with unit, integration and end-to-end tests, automation, continuous integration and release quality checks.'),
]

ADVANCED_LESSONS = {
    'advanced-python': [
        ('Object-Oriented Design and Composition', 'Classes combine state and behaviour. Use a class when several values and operations belong together. Prefer composition when one object uses another object rather than inheriting its entire interface. Keep each class focused on one responsibility, expose a small public interface, and validate important state at the boundary. Inheritance is useful for a genuine “is-a” relationship, but deep inheritance chains make changes difficult to reason about.\n\nA useful design process is to identify the responsibilities, decide which data each object owns, and define the messages objects exchange. Avoid making every attribute public when callers should use a method to preserve an invariant.', 'class Engine:\n    def start(self):\n        return "Engine started"\n\nclass Robot:\n    def __init__(self, engine):\n        self.engine = engine\n\n    def activate(self):\n        return self.engine.start()\n\nrobot = Robot(Engine())\nprint(robot.activate())'),
        ('Iterators, Generators and Lazy Evaluation', 'An iterable can produce an iterator. An iterator remembers its current position and supplies the next value when requested. A generator function uses yield to produce values one at a time, which is useful when a sequence is large or can be processed as a stream. Lazy evaluation avoids building an entire collection before it is needed.\n\nA generator is normally consumed once. If you need to traverse the data repeatedly, create a fresh generator or store the results deliberately. Be careful with resources such as files: use a context manager so they are closed even if iteration stops early.', 'def read_batches(records, batch_size):\n    for start in range(0, len(records), batch_size):\n        yield records[start:start + batch_size]\n\nfor batch in read_batches(list(range(10)), 3):\n    print(batch)'),
        ('Decorators and Context Managers', 'A decorator receives a function and returns a replacement function, often adding behaviour before or after the original call. functools.wraps preserves useful metadata such as the original function name. Decorators are commonly used for logging, timing, access checks and registration.\n\nA context manager controls setup and cleanup around a block. The with statement makes resource handling clearer and safer. Use context managers for files, locks and other resources that must be released reliably.', 'from functools import wraps\n\ndef announce(function):\n    @wraps(function)\n    def wrapper(*args, **kwargs):\n        print("Starting")\n        return function(*args, **kwargs)\n    return wrapper\n\n@announce\ndef greet(name):\n    return f"Hello, {name}"\n\nprint(greet("Ada"))'),
        ('Async Programming and Automated Testing', 'Asynchronous programming is useful when a task spends time waiting for network or file operations. async def defines a coroutine and await suspends it until an awaitable operation completes. It does not automatically make CPU-heavy work faster. Use asyncio.gather when independent waiting tasks can run concurrently, and handle exceptions and cancellation intentionally.\n\nTests should cover normal inputs, invalid inputs and boundary conditions. Keep units small, make dependencies replaceable, and test observable behaviour rather than private implementation details.', 'import asyncio\n\nasync def fetch_label(label):\n    await asyncio.sleep(0.1)\n    return f"Loaded: {label}"\n\nasync def main():\n    results = await asyncio.gather(\n        fetch_label("users"), fetch_label("courses")\n    )\n    print(results)\n\nasyncio.run(main())'),
    ],
    'flask-full-stack': [
        ('Application Structure and Configuration', 'A maintainable Flask project separates application setup, database models, routes, templates and configuration. An application factory makes it possible to create differently configured app instances for tests and production. Keep secrets outside source control, use environment variables for deployment configuration, and never expose secret values in HTML or logs.\n\nUse separate development and production settings. Production should have debug mode disabled, a strong stable secret key, HTTPS, secure cookies and a persistent database. Validate required configuration at startup so deployment errors are detected early.', 'import os\nfrom flask import Flask\n\ndef create_app():\n    app = Flask(__name__)\n    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]\n    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]\n    return app'),
        ('Relational Data, SQLAlchemy and Transactions', 'SQLAlchemy models describe relational data and relationships. Choose column types deliberately, add uniqueness and foreign-key constraints where they represent real rules, and index fields used frequently for filtering or joining. A database transaction groups related changes so they succeed or fail together.\n\nDo not assume a sequence of Python statements is automatically atomic. Commit after a coherent unit of work and roll back when an error occurs. For schema changes on an existing database, use migrations rather than relying on create_all(), which creates missing tables but does not update existing table definitions.', 'from sqlalchemy import select\n\n# Example query using a SQLAlchemy model named User\nstatement = select(User).where(User.email == email)\nuser = db.session.execute(statement).scalar_one_or_none()\n\ntry:\n    db.session.add(new_record)\n    db.session.commit()\nexcept Exception:\n    db.session.rollback()\n    raise'),
        ('Authentication, Authorisation and CSRF', 'Authentication establishes who a user is; authorisation decides what that user may do. Check permissions on the server for every protected page and API endpoint. Hiding a button in a template is not an access-control system because a client can request the URL directly. Apply least privilege and deny access by default.\n\nUse a proven password-hashing function, protect state-changing browser forms with CSRF tokens, validate input on the server, and avoid returning private records belonging to another account. For administrator privileges, use a trusted server-side role or configured identity, never a form field supplied by the visitor.', '@app.post("/admin/report")\n@login_required\ndef admin_report():\n    if not is_admin_user():\n        abort(403)\n    return jsonify(ok=True)'),
        ('REST APIs, Validation and Error Handling', 'An API should have predictable routes, methods, status codes and response shapes. Validate the JSON type and every field before using it. Return 400 for malformed input, 401 for unauthenticated requests, 403 for authenticated users without permission, and 404 when a resource should not be disclosed. Avoid returning stack traces or secrets to clients.\n\nMake state-changing operations safe against duplicate submissions where appropriate. Use database constraints and idempotency keys for payment-related workflows, and verify payment status with the payment provider on the server rather than trusting a browser redirect.', 'from flask import request, jsonify\n\n@app.post("/api/tasks")\n@login_required\ndef create_task():\n    data = request.get_json(silent=True) or {}\n    title = data.get("title")\n    if not isinstance(title, str) or not title.strip():\n        return jsonify(error="A title is required."), 400\n    return jsonify(ok=True, title=title.strip()), 201'),
        ('Testing, Deployment and Observability', 'Use automated tests for route permissions, form validation, database behaviour and payment verification. A test client can exercise routes without starting a public server. Use a separate test database and predictable test configuration.\n\nDeploy with debug disabled and secrets configured in the hosting provider. Keep database backups, monitor application errors, and log enough context to diagnose failures without recording passwords, payment secrets or sensitive personal data. Test migrations and rollback procedures before applying schema changes to production.', 'def test_private_route_requires_login(client):\n    response = client.get("/profile")\n    assert response.status_code in (302, 401)\n\ndef test_admin_route_denies_learner(authenticated_client):\n    response = authenticated_client.get("/admin")\n    assert response.status_code == 403'),
    ],
    'advanced-javascript': [
        ('Closures, Scope and Modules', 'A closure is a function together with access to variables from its lexical environment. Closures are useful for private state and function factories, but retained references can keep data in memory longer than expected. Prefer const by default and use let when reassignment is necessary.\n\nES modules organise code with export and import. Keep modules focused, avoid circular dependencies, and separate data access from interface code. Module boundaries make larger applications easier to test and maintain.', 'function createCounter() {\n  let count = 0;\n  return function increment() {\n    count += 1;\n    return count;\n  };\n}\n\nconst next = createCounter();\nconsole.log(next());\nconsole.log(next());'),
        ('Promises and Async/Await', 'A Promise represents the eventual result of an asynchronous operation. It may be pending, fulfilled or rejected. Use then/catch/finally or async/await to handle its outcome. Await pauses the current async function, not the entire browser. Handle errors at a useful boundary and do not silently discard rejected promises.\n\nWhen tasks are independent, Promise.all can run them concurrently and rejects if one input rejects. Promise.allSettled is useful when every result matters even if some tasks fail.', 'async function loadProfile() {\n  try {\n    const response = await fetch("/api/profile");\n    if (!response.ok) throw new Error("Request failed");\n    return await response.json();\n  } catch (error) {\n    console.error("Could not load profile", error);\n    throw error;\n  }\n}'),
        ('DOM Events and Accessible Interfaces', 'The DOM represents a document as nodes that JavaScript can inspect and update. Use addEventListener to respond to user actions. Event delegation attaches one listener to a stable parent and checks the event target, which can simplify dynamic lists.\n\nBuild controls with semantic HTML and preserve keyboard access. Use labels for form controls, meaningful button text, visible focus indicators and status messages that assistive technology can discover. Do not use colour as the only way to communicate an error or state.', 'document.querySelector("#task-list").addEventListener("click", (event) => {\n  const button = event.target.closest("button[data-action]");\n  if (!button) return;\n  if (button.dataset.action === "remove") {\n    button.closest("li")?.remove();\n  }\n});'),
        ('Testing and Performance', 'Test behaviour at the boundaries of a component. Unit tests are fast and focused; integration tests verify that modules work together; end-to-end tests exercise a complete user journey. Use deterministic test data and avoid tests that depend on timing or external services.\n\nMeasure before optimising. Reduce unnecessary DOM updates, avoid repeated expensive calculations, split large bundles when appropriate, and clean up event listeners or subscriptions when components are removed.', 'function calculateTotal(items) {\n  return items.reduce((total, item) => {\n    if (!Number.isFinite(item.price) || item.price < 0) {\n      throw new TypeError("Invalid price");\n    }\n    return total + item.price;\n  }, 0);\n}\n\nconsole.log(calculateTotal([{price: 10}, {price: 5}]));'),
    ],
    'database-engineering': [
        ('Relational Modelling and Normalisation', 'A relational database stores related facts in tables connected by keys. A primary key uniquely identifies a row; a foreign key references a row in another table. Normalisation reduces duplicated facts and update anomalies by separating entities and relationships into appropriate tables.\n\nModel real relationships carefully: one-to-one, one-to-many and many-to-many. For many-to-many relationships, use a junction table. Choose constraints that express business rules, and document any deliberate denormalisation used for performance.', 'CREATE TABLE students (\n    id INTEGER PRIMARY KEY,\n    full_name VARCHAR(120) NOT NULL\n);\n\nCREATE TABLE enrolments (\n    student_id INTEGER NOT NULL REFERENCES students(id),\n    course_id INTEGER NOT NULL,\n    PRIMARY KEY (student_id, course_id)\n);'),
        ('Indexes and Query Plans', 'An index helps the database locate rows without scanning every row, but indexes consume storage and add work to inserts, updates and deletes. Index columns used frequently in selective filters, joins and ordering. Composite index column order matters because databases can often use the leftmost prefix.\n\nUse EXPLAIN or the database query planner to inspect how a query is executed. Compare realistic data volumes and avoid adding indexes based only on guesswork.', 'CREATE INDEX idx_orders_customer_date\nON orders(customer_id, created_at);\n\nEXPLAIN\nSELECT id, created_at, total\nFROM orders\nWHERE customer_id = 42\nORDER BY created_at DESC;'),
        ('Transactions and Concurrency', 'A transaction groups operations into a single logical unit. ACID describes atomicity, consistency, isolation and durability. Isolation levels control how concurrent transactions observe one another. Locks and optimistic concurrency mechanisms help prevent conflicting updates.\n\nKeep transactions short, handle deadlocks with a bounded retry strategy, and enforce critical invariants with database constraints. Application-level checks alone can race when two requests arrive at nearly the same time.', 'BEGIN;\nUPDATE accounts SET balance = balance - 100 WHERE id = 1;\nUPDATE accounts SET balance = balance + 100 WHERE id = 2;\nCOMMIT;\n\n-- If a step fails, issue ROLLBACK instead.'),
        ('Safe Queries, Backups and Recovery', 'Use parameterised queries so user data is kept separate from SQL instructions. Never build a query by concatenating untrusted text. Apply least-privilege database accounts and keep credentials out of source code.\n\nA backup is useful only if it can be restored. Define recovery objectives, keep protected backup copies, test restoration regularly and understand how to recover from accidental deletion or corruption.', 'cursor.execute(\n    "SELECT id, full_name FROM students WHERE email = ?",\n    (email,)\n)\n\n# The parameter is data, not executable SQL.'),
    ],
    'data-structures-algorithms': [
        ('Algorithm Analysis and Big-O', 'Algorithm analysis estimates how running time or memory grows as input size grows. Big-O describes an upper growth bound and helps compare approaches as data becomes large. Constant, logarithmic, linear, linearithmic, quadratic and exponential growth behave very differently.\n\nAnalyse the dominant operation and state assumptions. An algorithm with a lower asymptotic cost may still be slower for tiny inputs because of constants and implementation overhead, so measure realistic workloads too.', 'def contains_value(items, target):\n    for item in items:       # at most n comparisons\n        if item == target:\n            return True\n    return False              # O(n) time, O(1) extra space'),
        ('Stacks, Queues and Linked Structures', 'A stack follows last-in, first-out order; a queue follows first-in, first-out order. They are useful for undo operations, parsing, task scheduling and breadth-first search. A linked list stores nodes connected by references, which can make insertion at a known position efficient but makes random access slower than an array.\n\nChoose a structure based on the operations the application needs, not simply on its name. In Python, collections.deque is a good general-purpose queue.', 'from collections import deque\n\nqueue = deque(["task A", "task B"])\nqueue.append("task C")\nnext_task = queue.popleft()\nprint(next_task)'),
        ('Searching and Sorting', 'Linear search checks items one by one and works on unsorted data. Binary search repeatedly halves a sorted search interval and takes logarithmic time. Sorting algorithms trade off time, memory, stability and implementation complexity.\n\nBinary search requires a correctly sorted sequence and careful boundary handling. Prefer a well-tested standard-library sort unless learning or a special constraint requires implementing one yourself.', 'def binary_search(values, target):\n    low, high = 0, len(values) - 1\n    while low <= high:\n        mid = (low + high) // 2\n        if values[mid] == target:\n            return mid\n        if values[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1'),
        ('Trees, Graphs and Traversal', 'A tree is a hierarchical structure with nodes and edges. A binary search tree orders values so that lookup can be efficient when the tree is balanced. A graph models general relationships and may be directed, undirected, weighted or unweighted.\n\nDepth-first search explores a path before backtracking; breadth-first search explores neighbours in layers. Breadth-first search finds shortest paths in an unweighted graph. Track visited nodes to avoid repeated work and infinite traversal on cyclic graphs.', 'from collections import deque\n\ndef bfs(graph, start):\n    visited = {start}\n    queue = deque([start])\n    order = []\n    while queue:\n        node = queue.popleft()\n        order.append(node)\n        for neighbour in graph[node]:\n            if neighbour not in visited:\n                visited.add(neighbour)\n                queue.append(neighbour)\n    return order'),
    ],

    'react-frontend-architecture': [
        ('Component Design and Props', 'A React component should represent a clear piece of interface or behaviour. Keep components focused, give them descriptive names, and pass information through props. Props are read-only inputs: a child should not mutate values owned by its parent. Prefer composition when a screen needs several related pieces, and avoid turning every small element into a component when doing so makes the structure harder to follow.\n\nA useful component boundary is one that can be understood, tested and reused without needing to know the entire page. Use semantic HTML inside components and provide labels for interactive controls.', 'function ProfileCard({ name, role }) {\n  return (\n    <article className="profile-card">\n      <h2>{name}</h2>\n      <p>{role}</p>\n    </article>\n  );\n}\n\nexport default ProfileCard;'),
        ('State, Events and Derived UI', 'State represents information that can change while a component is in use. Use the state setter to request an update; do not mutate state objects directly. Keep state as close as practical to the components that need it. If a value can be calculated from existing props or state, derive it during rendering rather than storing a duplicate that can become inconsistent.\n\nEvent handlers should describe the user action they handle. For forms, track the input value, validate it, and provide clear feedback. For complex shared state, consider a reducer or a dedicated state-management approach rather than passing many unrelated setters through the component tree.', 'import { useState } from "react";\n\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  return (\n    <button onClick={() => setCount(value => value + 1)}>\n      Count: {count}\n    </button>\n  );\n}'),
        ('Effects, Data Fetching and Cleanup', 'Effects synchronise a component with something outside React, such as a browser API or subscription. They are not a general place to calculate values that can be derived during rendering. Include every reactive value used by an effect in its dependency list. When an effect starts a subscription or request, clean it up when the component no longer needs it.\n\nFor network requests, represent loading, success and error states. Avoid allowing an older request to overwrite newer results when the user changes the search or selected record quickly. For larger applications, use a data-fetching library or framework facilities that handle caching and request lifecycles.', 'import { useEffect, useState } from "react";\n\nfunction Status() {\n  const [online, setOnline] = useState(navigator.onLine);\n  useEffect(() => {\n    const update = () => setOnline(navigator.onLine);\n    window.addEventListener("online", update);\n    window.addEventListener("offline", update);\n    return () => {\n      window.removeEventListener("online", update);\n      window.removeEventListener("offline", update);\n    };\n  }, []);\n  return <p>{online ? "Online" : "Offline"}</p>;\n}'),
        ('Accessibility, Performance and Testing', 'Accessible interfaces work with keyboards, screen readers and different input methods. Use native buttons and links, associate labels with fields, preserve visible focus, and communicate errors in text rather than colour alone. Measure performance before optimising. Large lists may need pagination or virtualisation, and expensive calculations may need memoisation only when measurement shows a benefit.\n\nTest components through the behaviour users can observe: what appears, what happens after an interaction, and what is announced to assistive technology. Avoid tests that depend heavily on private implementation details.', 'import { render, screen } from "@testing-library/react";\nimport userEvent from "@testing-library/user-event";\nimport Counter from "./Counter";\n\ntest("increments when clicked", async () => {\n  const user = userEvent.setup();\n  render(<Counter />);\n  await user.click(screen.getByRole("button"));\n  expect(screen.getByRole("button")).toHaveTextContent("1");\n});'),
    ],
    'api-engineering': [
        ('Resource-Oriented API Design', 'A well-designed REST API exposes resources through predictable URLs and uses HTTP methods consistently. GET retrieves data, POST creates or initiates work, PUT replaces a resource, PATCH changes selected fields and DELETE removes a resource when appropriate. Use status codes that communicate the outcome, and return a consistent response structure.\n\nKeep internal database structure separate from public response schemas. Add pagination to collections, filtering for common queries and stable ordering so clients can navigate large result sets. Document required fields, optional fields, error responses and authentication requirements.', 'from flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.get("/api/v1/courses")\ndef list_courses():\n    return jsonify(data=[], page=1, per_page=20, total=0)'),
        ('Validation, Serialisation and Error Contracts', 'Treat every client-supplied value as untrusted, even when the browser interface already validates it. Check types, lengths, allowed values and relationships between fields on the server. Reject malformed JSON and unexpected fields deliberately. Serialise only fields the caller is allowed to see; never return password hashes, private tokens or internal configuration.\n\nUse a shared error format so clients can handle failures predictably. Avoid exposing stack traces or database messages. Log technical details on the server while returning a safe, actionable message to the client.', 'from flask import request, jsonify\n\ndef parse_title(data):\n    title = data.get("title") if isinstance(data, dict) else None\n    if not isinstance(title, str) or not title.strip():\n        return None, (jsonify(error={"code": "invalid_title",\n                                    "message": "A title is required."}), 400)\n    return title.strip()[:120], None'),
        ('Authentication, Rate Limits and Pagination', 'Choose authentication that fits the client and threat model. Browser applications commonly use secure sessions; service integrations may use scoped tokens. Apply authorisation to every resource lookup, not just to the page that links to it. A user should not gain access to another user\'s record by changing an identifier in a URL.\n\nRate limits reduce accidental overload and abuse. Apply limits to expensive or sensitive operations, and return a retry hint when possible. Pagination should have a maximum page size and a deterministic sort order. Validate page and cursor values before querying the database.', 'def page_args(args):\n    try:\n        page = max(1, int(args.get("page", 1)))\n        per_page = min(100, max(1, int(args.get("per_page", 20))))\n    except (TypeError, ValueError):\n        page, per_page = 1, 20\n    return page, per_page'),
        ('API Testing and Documentation', 'API tests should cover success, invalid input, unauthenticated requests, insufficient permissions, missing records and boundary conditions. Use a test database and create fixtures that represent different user roles. Test the response status, JSON schema and important side effects.\n\nOpenAPI provides a machine-readable description of routes, parameters, schemas and responses. Keep documentation close to the code and update it whenever the contract changes. Include example requests and responses, but never use real passwords, API keys or private customer data in examples.', 'def test_list_courses_returns_json(client):\n    response = client.get("/api/v1/courses")\n    assert response.status_code == 200\n    payload = response.get_json()\n    assert "data" in payload\n    assert isinstance(payload["data"], list)'),
    ],
    'cloud-devops-engineering': [
        ('Environments, Configuration and Secrets', 'Applications behave differently across development, test and production because their configuration differs. Keep configuration outside the code and read it from environment variables or a managed secret store. Validate required values at startup and fail clearly if a critical setting is missing. Never commit credentials to a repository or print them in logs.\n\nUse separate databases and credentials for test and production. Keep a stable application secret across deployments when sessions or signed tokens depend on it. Rotate exposed secrets and review access permissions regularly.', 'import os\n\nconfig = {\n    "debug": os.getenv("APP_DEBUG", "false").lower() == "true",\n    "database_url": os.environ["DATABASE_URL"],\n}\nif config["debug"] and os.getenv("APP_ENV") == "production":\n    raise RuntimeError("Debug mode must be disabled in production")'),
        ('Containers and Reproducible Builds', 'A container packages an application with its runtime dependencies so it can run consistently across environments. Keep images small, use a supported base image, pin dependencies where appropriate and run the process as a non-root user. Do not bake secrets into image layers.\n\nA reproducible build starts from version-controlled source and produces a predictable artifact. Separate build-time dependencies from runtime dependencies when practical, and scan dependencies for known vulnerabilities. A container is not a complete security boundary: the host, network and runtime configuration still matter.', 'FROM python:3.12-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install --no-cache-dir -r requirements.txt\nCOPY . .\nRUN useradd --create-home appuser\nUSER appuser\nCMD ["gunicorn", "app:app"]'),
        ('Continuous Delivery and Safe Releases', 'A deployment pipeline can run formatting checks, static analysis, tests and build steps before publishing an application. Make the pipeline fail when a required quality check fails. Keep deployment credentials in the platform secret store and grant the pipeline only the permissions it needs.\n\nUse health checks and a rollback plan. Database migrations should be compatible with the currently running version during rolling deployments. Prefer small, reversible changes and verify the application after release rather than assuming that a successful build means the service is healthy.', 'name: test-and-build\non:\n  push:\n    branches: [main]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: "3.12"\n      - run: pip install -r requirements.txt\n      - run: python -m compileall -q .'),
        ('Monitoring, Logs and Reliability', 'Monitoring helps distinguish an application failure from a dependency or infrastructure failure. Track request rates, error rates, latency and resource use. Health endpoints should report whether the service can handle traffic, while readiness checks can verify critical dependencies.\n\nLogs should be structured and useful for troubleshooting, but must not contain passwords, payment secrets or unnecessary personal data. Define backup and restore procedures, test them, and decide how the service should behave when an external dependency is unavailable.', 'import logging\nlogger = logging.getLogger(__name__)\n\ndef record_job_result(job_name, succeeded):\n    logger.info("job_finished", extra={\n        "job_name": job_name,\n        "succeeded": bool(succeeded),\n    })'),
    ],
    'secure-web-engineering': [
        ('Trust Boundaries and Input Validation', 'Security starts by identifying trust boundaries: browser input, uploaded files, external APIs, databases and administrative actions. Validate input on the server using explicit rules for type, length and allowed values. Use parameterised database queries or an ORM rather than assembling SQL with string concatenation. Encode output for the context where it is displayed.\n\nValidation and output encoding solve different problems. Validation checks whether input is acceptable for the application; encoding ensures data is treated as data rather than executable markup in the output context.', 'from flask import request, abort\n\ndef read_display_name():\n    value = request.form.get("display_name", "")\n    if not isinstance(value, str) or not 1 <= len(value.strip()) <= 60:\n        abort(400)\n    return value.strip()'),
        ('Session Security and Access Control', 'A session should be protected against theft and misuse. Use HTTPS, secure and HTTP-only cookies, an appropriate same-site policy and a strong secret key. Regenerate or clear session state after authentication changes. Keep session lifetimes appropriate to the sensitivity of the application.\n\nAuthorisation must be enforced on the server for every protected route and object. Check ownership when a user requests a record, and check privileged roles using trusted server-side information. Hiding navigation links is useful for interface clarity but is never a substitute for backend permission checks.', 'app.config.update(\n    SESSION_COOKIE_SECURE=True,\n    SESSION_COOKIE_HTTPONLY=True,\n    SESSION_COOKIE_SAMESITE="Lax",\n)\n\ndef can_edit_record(user, record):\n    return user.is_authenticated and record.owner_id == user.id'),
        ('CSRF, XSS and Safe File Handling', 'Cross-site request forgery protection helps ensure that a state-changing browser request was intentionally submitted from the application. Cross-site scripting prevention requires context-aware output encoding and careful handling of HTML. Avoid inserting untrusted strings into innerHTML; prefer textContent or a trusted templating system with escaping enabled.\n\nFor file uploads, enforce size limits, allow only necessary file types, generate server-side filenames, store files outside executable web roots and do not trust the supplied MIME type alone. Consider malware scanning where the application and risk justify it.', 'from pathlib import Path\nfrom werkzeug.utils import secure_filename\n\ndef safe_upload_name(original_name):\n    name = secure_filename(original_name)\n    if not name or Path(name).suffix.lower() not in {".txt", ".pdf"}:\n        raise ValueError("Unsupported file type")\n    return name'),
        ('Security Review and Dependency Hygiene', 'Security is an ongoing engineering practice. Keep frameworks and dependencies supported, review release notes and update vulnerable packages. Remove unused packages and permissions. Use dependency lock files and test updates before production.\n\nCreate a checklist for authentication, authorisation, data validation, error handling, logging, backups and secret management. Review high-risk changes before release, and provide a clear process for reporting and fixing defects. Never test against systems or accounts unless you have explicit permission.', 'from importlib.metadata import version, PackageNotFoundError\n\ndef package_version(name):\n    try:\n        return version(name)\n    except PackageNotFoundError:\n        return "not installed"\n\nprint(package_version("flask"))'),
    ],
    'machine-learning-python': [
        ('Data Preparation and Feature Design', 'Machine-learning systems learn patterns from examples, so data quality strongly affects the result. Inspect missing values, duplicates, incorrect types and unusual ranges before training. Split data into training and test sets before fitting transformations to avoid leaking information from the test set into training.\n\nFeatures should represent useful information available at prediction time. Avoid including fields that reveal the target answer or information that would not exist when the model is used. Record how data was collected and any limitations that affect interpretation.', 'from sklearn.model_selection import train_test_split\n\nX_train, X_test, y_train, y_test = train_test_split(\n    features, labels, test_size=0.2, random_state=42\n)'),
        ('Training a Baseline Model', 'Start with a simple baseline so you have a reference point for later improvements. Choose an algorithm that fits the data and task, then train it only on the training set. Keep preprocessing steps consistent between training and prediction. A pipeline can combine transformations and an estimator so they are applied in the correct order.\n\nDo not select a model only because it is complex. A simpler model may be easier to explain, maintain and validate, and may perform just as well on new data.', 'from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.linear_model import LogisticRegression\n\nmodel = make_pipeline(StandardScaler(), LogisticRegression())\nmodel.fit(X_train, y_train)'),
        ('Evaluation, Overfitting and Model Selection', 'Evaluate with data the model did not use for fitting. The metric should match the problem: accuracy can be misleading for imbalanced classes, while precision, recall, F1 and a confusion matrix reveal different error patterns. For regression, metrics such as mean absolute error and root mean squared error measure prediction differences.\n\nOverfitting occurs when a model captures noise in the training data and performs poorly on new examples. Use cross-validation and a separate test set, tune hyperparameters without repeatedly checking the test set, and compare against the baseline.', 'from sklearn.metrics import classification_report\n\npredictions = model.predict(X_test)\nprint(classification_report(y_test, predictions))'),
        ('Reproducibility and Responsible Use', 'A model experiment should record the dataset version, feature choices, preprocessing, algorithm, parameters, random seed and evaluation results. Reproducibility makes it easier to understand why a model changed and whether an improvement is genuine.\n\nModels can reflect bias in their training data and may fail when conditions change. Check performance across relevant groups, protect private data, explain limitations and provide human review when decisions have meaningful consequences. Do not treat a model score as proof that a system is fair or reliable.', 'experiment = {\n    "dataset_version": "v1",\n    "random_seed": 42,\n    "model": "logistic_regression",\n    "metric": "f1",\n    "notes": "Baseline experiment; document limitations."\n}\nprint(experiment)'),
    ],
    'software-testing-cicd': [
        ('Unit Tests and Testable Design', 'Unit tests check a small piece of behaviour in isolation. A good unit test has a clear arrangement, action and assertion. Test normal cases, invalid values and boundaries. Keep tests deterministic by controlling time, randomness and external dependencies.\n\nCode becomes easier to test when responsibilities are separated and dependencies can be supplied from the outside. Avoid making tests depend on network services or a production database. A focused test should explain the expected behaviour when it fails.', 'def calculate_total(prices):\n    if any(price < 0 for price in prices):\n        raise ValueError("Prices cannot be negative")\n    return sum(prices)\n\ndef test_calculate_total():\n    assert calculate_total([10, 5, 2]) == 17'),
        ('Integration Tests and Test Data', 'Integration tests check whether components work together, such as a route and database or a service and its repository. Use a separate test database and create only the records required for each test. Clean up after tests so one test cannot accidentally affect another.\n\nTest both successful operations and failures such as missing records, invalid relationships and permission denials. For web applications, a framework test client can exercise routes without running a public server.', 'def test_create_record(client, auth_headers):\n    response = client.post(\n        "/api/records",\n        json={"title": "Example"},\n        headers=auth_headers,\n    )\n    assert response.status_code == 201\n    assert response.get_json()["title"] == "Example"'),
        ('Continuous Integration Quality Gates', 'Continuous integration runs repeatable checks whenever code changes. Typical steps include installing dependencies, formatting checks, linting, static analysis, unit tests and building the application. A quality gate prevents a change from being merged when required checks fail.\n\nKeep the pipeline fast enough that developers use it consistently. Cache dependencies when safe, split independent checks into jobs and store logs for failed runs. Never expose deployment secrets to untrusted pull-request code.', 'name: python-checks\non: [push, pull_request]\njobs:\n  tests:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - uses: actions/setup-python@v5\n        with:\n          python-version: "3.12"\n      - run: pip install -r requirements.txt\n      - run: python -m compileall -q .\n      - run: pytest'),
        ('Release Verification and Regression Testing', 'A regression test protects behaviour that previously worked. When fixing a defect, first create a test that demonstrates the problem, then implement the correction and confirm the test passes. Before release, check migrations, configuration, health checks and the most important user journeys.\n\nA deployment should have a clear owner, a release note and a rollback strategy. Monitor error rates and key workflows after release. If a release causes a serious issue, restore service first and investigate the root cause afterwards.', 'def test_membership_expiry_denies_advanced_access(client, expired_user):\n    login_as(client, expired_user)\n    response = client.get("/advanced-courses/advanced-python")\n    assert response.status_code in (200, 302)\n    # The locked response must not contain lesson-body content.\n    assert b"Premium access required" in response.data'),
    ],
}

ADVANCED_QUIZ_BANK = {
    'advanced-python': [
        ('Which design approach favours using a contained object instead of inheriting its entire interface?', ['Composition', 'Global state', 'Multiple assignment', 'Recursion'], 0, 'Composition models a has-a relationship and keeps responsibilities separate.'),
        ('What does a generator yield?', ['All values at once', 'One value at a time on request', 'Only strings', 'A compiled module'], 1, 'Generators produce values lazily as iteration requests them.'),
        ('What is the purpose of functools.wraps in a decorator?', ['To encrypt a function', 'To preserve wrapped function metadata', 'To create a thread', 'To cache every result'], 1, 'wraps preserves metadata such as the original function name and documentation.'),
    ],
    'flask-full-stack': [
        ('Where should production secrets be stored?', ['In a public template', 'In source control', 'In environment variables or a secret manager', 'In a URL query string'], 2, 'Secrets belong in protected deployment configuration, not in source code or the browser.'),
        ('What does a database transaction provide?', ['A way to group related changes atomically', 'Automatic HTML escaping', 'A CSS layout', 'A browser session'], 0, 'Transactions allow related changes to commit together or roll back.'),
        ('Where must authorisation be enforced?', ['Only in the navigation bar', 'On the server for every protected action', 'Only in JavaScript', 'Only on the homepage'], 1, 'Client-side hiding is not security; the server must check every protected request.'),
    ],
    'advanced-javascript': [
        ('What is a closure?', ['A function with access to its lexical scope', 'A closed browser tab', 'A CSS selector', 'A JSON file'], 0, 'A closure retains access to variables from its surrounding lexical environment.'),
        ('What does Promise.all do?', ['Runs independent promises and waits for all to settle successfully', 'Converts JavaScript to CSS', 'Stops the event loop', 'Creates a module'], 0, 'Promise.all fulfils when all input promises fulfil and rejects if one rejects.'),
        ('Why use JavaScript modules?', ['To share code through explicit imports and exports', 'To disable functions', 'To remove types from data', 'To replace HTML'], 0, 'Modules define explicit boundaries for reusable code.'),
    ],
    'database-engineering': [
        ('What is a database index mainly used for?', ['Speeding up suitable lookups', 'Encrypting passwords', 'Replacing backups', 'Removing constraints'], 0, 'Indexes can improve retrieval speed, with storage and write-performance trade-offs.'),
        ('What does atomicity mean in a transaction?', ['All operations happen or none do', 'Queries always run in alphabetical order', 'Every table has one column', 'Data is automatically compressed'], 0, 'Atomicity prevents a transaction from being partially applied.'),
        ('Why normalise relational data?', ['To reduce unwanted duplication and update anomalies', 'To make every query slower', 'To remove primary keys', 'To store images only'], 0, 'Normalisation organises data to reduce redundancy and anomalies.'),
    ],
    'data-structures-algorithms': [
        ('What prerequisite does binary search require?', ['A sorted search sequence', 'A linked list only', 'A graph with cycles', 'A random pivot'], 0, 'Binary search relies on sorted order to discard half of the remaining range.'),
        ('Which structure follows first-in, first-out order?', ['Stack', 'Queue', 'Tree', 'Set'], 1, 'A queue processes the earliest added item first.'),
        ('Which traversal finds shortest paths in an unweighted graph?', ['Depth-first search', 'Breadth-first search', 'Inorder traversal', 'Binary insertion'], 1, 'Breadth-first search explores vertices in layers.'),
    ],
    'react-frontend-architecture': [
        ('How should a React component treat props?', ['As read-only inputs', 'As global variables', 'As values to mutate directly', 'As database rows'], 0, 'Props are inputs supplied by a parent and should not be mutated by the child.'),
        ('What should be used to update React state?', ['Direct object mutation', 'The state setter', 'A CSS class', 'A console log'], 1, 'Use the setter so React can schedule and render the update.'),
        ('What should an effect do when it starts a subscription?', ['Leave it running forever', 'Return cleanup logic', 'Change every prop', 'Disable rendering'], 1, 'Cleanup removes subscriptions when the effect is replaced or the component unmounts.'),
    ],
    'api-engineering': [
        ('Which HTTP method is commonly used to retrieve a resource?', ['POST', 'GET', 'PATCH', 'DELETE'], 1, 'GET retrieves a representation of a resource.'),
        ('Why validate API input on the server?', ['Browser validation can be bypassed', 'It improves CSS', 'It hides the route', 'It removes the need for authentication'], 0, 'All client input is untrusted and must be validated by the server.'),
        ('What is pagination used for?', ['Splitting large result sets into manageable pages', 'Encrypting API responses', 'Replacing authorisation', 'Changing HTTP methods'], 0, 'Pagination limits response sizes and helps clients navigate collections.'),
    ],
    'cloud-devops-engineering': [
        ('Where should deployment credentials be stored?', ['In a committed config file', 'In the platform secret store', 'In a public issue', 'In client-side JavaScript'], 1, 'A protected secret store limits exposure and access.'),
        ('What is a container image?', ['A packaged application filesystem and runtime setup', 'A screenshot of a server', 'A database index', 'A browser cookie'], 0, 'Container images provide a repeatable artifact for running an application.'),
        ('Why use a health check after deployment?', ['To confirm the service is functioning', 'To rename the domain', 'To replace tests', 'To disable logs'], 0, 'Health checks help detect whether the deployed service is ready and operating.'),
    ],
    'secure-web-engineering': [
        ('What is the purpose of CSRF protection?', ['To help verify intentional state-changing browser requests', 'To speed up SQL queries', 'To compress images', 'To create user roles'], 0, 'CSRF protection helps prevent unwanted cross-site form submissions.'),
        ('What should be done with untrusted text before inserting it into a page?', ['Use context-appropriate output encoding', 'Treat it as trusted HTML', 'Put it into a script tag', 'Disable all validation'], 0, 'Output encoding helps ensure data is displayed as data, not executable markup.'),
        ('Which cookie flag prevents JavaScript from reading a session cookie?', ['HttpOnly', 'Public', 'Index', 'Cache'], 0, 'HttpOnly prevents access to the cookie through browser JavaScript.'),
    ],
    'machine-learning-python': [
        ('Why split data into training and test sets?', ['To evaluate generalisation on unseen examples', 'To duplicate every row', 'To guarantee perfect accuracy', 'To remove the need for metrics'], 0, 'A held-out test set estimates performance on data not used for fitting.'),
        ('What is overfitting?', ['Learning noise in training data and performing poorly on new data', 'Using too few columns in a table', 'A model loading slowly', 'A missing Python package'], 0, 'An overfit model memorises training patterns that do not generalise.'),
        ('Why use a pipeline for preprocessing and modelling?', ['To apply steps consistently in the correct order', 'To avoid splitting data', 'To remove all features', 'To guarantee fairness'], 0, 'Pipelines keep transformations and estimators together during fitting and prediction.'),
    ],
    'software-testing-cicd': [
        ('What does a unit test usually check?', ['A small unit of behaviour in isolation', 'The entire public internet', 'A production payment card', 'Only page colours'], 0, 'Unit tests focus on a small function or component.'),
        ('What is a regression test?', ['A test that protects previously working behaviour', 'A test that deletes the database', 'A performance dashboard', 'A deployment secret'], 0, 'Regression tests help ensure a defect does not return.'),
        ('What is a CI quality gate?', ['A required check that must pass before a change proceeds', 'A login page', 'A database password', 'A manual code comment'], 0, 'Quality gates stop changes from proceeding when required checks fail.'),
    ],
}

def is_admin_user():
    """Use the same configured administrator identity as the existing admin area."""
    admin_email = app.config.get('ADMIN_EMAIL', '')
    return bool(
        current_user.is_authenticated
        and app.config.get('ADMIN_ENABLED')
        and admin_email
        and current_user.email.lower() == admin_email
    )

def community_restriction_for(user_id):
    return CommunityRestriction.query.filter_by(user_id=user_id).first()

def ensure_community_access():
    restriction = community_restriction_for(current_user.id)
    if restriction:
        return render_template('community_blocked.html', restriction=restriction), 403
    return None

def are_users_mutually_blocked(user_id):
    """Return True if either learner has blocked the other.

    Community blocks are mutual for visibility: neither learner can see the
    other's discussions or replies while the block record exists.
    """
    if user_id == current_user.id:
        return False
    return CommunityUserBlock.query.filter(
        ((CommunityUserBlock.blocker_id == current_user.id) &
         (CommunityUserBlock.blocked_id == user_id)) |
        ((CommunityUserBlock.blocker_id == user_id) &
         (CommunityUserBlock.blocked_id == current_user.id))
    ).first() is not None

def has_active_premium_membership(user_id):
    now = datetime.utcnow()
    return MembershipPayment.query.filter(
        MembershipPayment.user_id == user_id,
        MembershipPayment.plan.in_(['monthly', 'annual']),
        MembershipPayment.status == 'paid',
        MembershipPayment.starts_at.isnot(None),
        MembershipPayment.starts_at <= now,
        MembershipPayment.ends_at.isnot(None),
        MembershipPayment.ends_at > now,
    ).first() is not None

def can_access_advanced_courses():
    return bool(current_user.is_authenticated and (
        is_admin_user() or has_active_premium_membership(current_user.id)
    ))

def course_is_premium(course):
    return getattr(course, 'access_level', 'free') == 'premium'

def enforce_course_access(course):
    if course_is_premium(course) and not can_access_advanced_courses():
        abort(403)

def seed_advanced_courses():
    for slug, title, language, level, description in ADVANCED_COURSE_SEED:
        course = Course.query.filter_by(slug=slug).first()
        if course is None:
            course = Course(slug=slug, title=title, language=language,
                            level=level, description=description, access_level='premium')
            db.session.add(course)
            db.session.flush()
        else:
            course.title, course.language = title, language
            course.level, course.description = level, description
            course.access_level = 'premium'
        existing = {lesson.position: lesson for lesson in course.lessons}
        for position, (title_text, body, example) in enumerate(ADVANCED_LESSONS.get(slug, []), 1):
            lesson = existing.get(position)
            if lesson is None:
                db.session.add(Lesson(course_id=course.id, title=title_text,
                                      body=body, example=example, position=position))
            else:
                lesson.title, lesson.body, lesson.example = title_text, body, example
        existing_questions = {question.position: question for question in QuizQuestion.query.filter_by(course_slug=slug).all()}
        for position, (prompt, options, correct, explanation) in enumerate(ADVANCED_QUIZ_BANK.get(slug, []), 1):
            question = existing_questions.get(position)
            if question is None:
                db.session.add(QuizQuestion(course_slug=slug, prompt=prompt,
                    options_json=json.dumps(options), correct_index=correct,
                    explanation=explanation, position=position))
            else:
                question.prompt = prompt
                question.options_json = json.dumps(options)
                question.correct_index = correct
                question.explanation = explanation
    db.session.commit()

@app.context_processor
def inject_globals():
    unread=Notification.query.filter_by(user_id=current_user.id,is_read=False).count() if current_user.is_authenticated else 0
    advanced_nav_active = request.endpoint in {'advanced_courses', 'advanced_course_detail'}
    view_args = request.view_args or {}
    if request.endpoint in {'course_detail', 'course_practice'} and view_args.get('slug'):
        current_course = Course.query.filter_by(slug=view_args['slug']).first()
        advanced_nav_active = bool(current_course and course_is_premium(current_course))
    elif request.endpoint == 'lesson_detail' and view_args.get('lesson_id'):
        current_lesson = db.session.get(Lesson, view_args['lesson_id'])
        advanced_nav_active = bool(current_lesson and current_lesson.course and course_is_premium(current_lesson.course))
    return {'year':datetime.utcnow().year, 'copyright_name':'Felix Saviour Oluebubechukwu',
            'unread_notifications':unread, 'advanced_nav_active':advanced_nav_active}

@app.before_request
def record_daily_activity():
    # Count a learner once per UTC day. This avoids a log row for every page view.
    if current_user.is_authenticated and request.endpoint not in {'static', 'logout'}:
        today = datetime.utcnow().date()
        activity = UserActivity.query.filter_by(user_id=current_user.id, activity_date=today).first()
        if activity is None:
            db.session.add(UserActivity(user_id=current_user.id, activity_date=today, last_seen_at=datetime.utcnow()))
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            app.logger.exception('Could not record learner activity')

@app.route('/')
def home():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    return render_template('landing.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method=='POST':
        username=request.form.get('username','').strip(); email=request.form.get('email','').strip().lower(); password=request.form.get('password',''); confirm_password=request.form.get('confirm_password','')
        if email == app.config.get('ADMIN_EMAIL') and not User.query.filter_by(email=email).first(): flash('The administrator account is created by the site owner, not through public sign-up.','error')
        elif not 3<=len(username)<=32 or not username.replace('_','').isalnum(): flash('Use a username of 3–32 letters, numbers or underscores.','error')
        elif '@' not in email or len(email)>254: flash('Enter a valid email address.','error')
        elif len(password)<10: flash('Use a password with at least 10 characters.','error')
        elif password != confirm_password: flash('Your passwords do not match. Please confirm your password.','error')
        elif User.query.filter((User.username==username)|(User.email==email)).first(): flash('That username or email is already registered.','error')
        else:
            user=User(username=username,email=email); user.set_password(password); db.session.add(user); db.session.flush(); db.session.add(MembershipPayment(user_id=user.id,plan='free',amount_kobo=0,status='active',starts_at=datetime.utcnow())); db.session.commit(); login_user(user, remember=True); session.permanent=True; flash('Your account is ready. Welcome!','success'); return redirect(url_for('dashboard'))
    return render_template('auth.html',mode='signup')

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated: return redirect(url_for('dashboard'))
    if request.method=='POST':
        identity=request.form.get('identity','').strip(); password=request.form.get('password','')
        user=User.query.filter((User.email==identity.lower())|(User.username==identity)).first()
        if user and user.check_password(password): login_user(user, remember=True); session.permanent=True; return redirect(url_for('dashboard'))
        flash('Login details were not recognised.','error')
    return render_template('auth.html',mode='login')

@app.post('/logout')
@login_required
def logout(): logout_user(); flash('You have logged out.','success'); return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    can_view_premium = can_access_advanced_courses()
    course_query = Course.query
    lesson_query = Lesson.query.join(Course)
    progress_query = Progress.query.filter_by(user_id=current_user.id).join(Lesson).join(Course)
    if not can_view_premium:
        course_query = course_query.filter(Course.access_level == 'free')
        lesson_query = lesson_query.filter(Course.access_level == 'free')
        progress_query = progress_query.filter(Course.access_level == 'free')
    courses = course_query.order_by(Course.title).all()
    completed = progress_query.count()
    total = lesson_query.count()
    projects=Project.query.filter_by(user_id=current_user.id).count(); all_results=QuizResult.query.filter_by(user_id=current_user.id).all(); accuracy=round(sum(r.score for r in all_results)/sum(r.total for r in all_results)*100) if all_results else 0; results=QuizResult.query.filter_by(user_id=current_user.id).order_by(QuizResult.created_at.desc()).limit(5).all()
    recent=Project.query.filter_by(user_id=current_user.id).order_by(Project.updated_at.desc()).limit(4).all()
    activity_dates=sorted({p.completed_at.date() for p in Progress.query.filter_by(user_id=current_user.id).all()},reverse=True)
    streak=0; today=date.today(); cursor=today if activity_dates and activity_dates[0]==today else today-timedelta(days=1)
    for day in activity_dates:
        if day==cursor: streak+=1; cursor-=timedelta(days=1)
        elif day<cursor: break
    return render_template('dashboard.html',courses=courses,completed=completed,total=total,projects=projects,accuracy=accuracy,results=results,recent=recent,streak=streak)

@app.route('/courses')
@login_required
def courses():
    visible_courses = Course.query.filter_by(access_level='free').order_by(Course.title).all()
    if can_access_advanced_courses():
        visible_courses += Course.query.filter_by(access_level='premium').order_by(Course.title).all()
    return render_template('courses.html', courses=visible_courses)

@app.route('/advanced-courses')
@login_required
def advanced_courses():
    items = Course.query.filter_by(access_level='premium').order_by(Course.title).all()
    return render_template('advanced_courses.html', courses=items, can_access=can_access_advanced_courses(),
                           monthly_fee=app.config['MEMBERSHIP_MONTHLY_NAIRA'],
                           annual_fee=app.config['MEMBERSHIP_ANNUAL_NAIRA'])

@app.route('/advanced-courses/<slug>')
@login_required
def advanced_course_detail(slug):
    course = Course.query.filter_by(slug=slug, access_level='premium').first_or_404()
    if can_access_advanced_courses():
        done = {p.lesson_id for p in Progress.query.filter_by(user_id=current_user.id).all()}
        return render_template('course.html', course=course, done=done)
    return render_template('advanced_course_locked.html', course=course,
                           monthly_fee=app.config['MEMBERSHIP_MONTHLY_NAIRA'],
                           annual_fee=app.config['MEMBERSHIP_ANNUAL_NAIRA'])

@app.route('/courses/<slug>')
@login_required
def course_detail(slug):
    course=Course.query.filter_by(slug=slug).first_or_404()
    if course_is_premium(course) and not can_access_advanced_courses():
        return redirect(url_for('advanced_course_detail', slug=slug))
    done={p.lesson_id for p in Progress.query.filter_by(user_id=current_user.id).all()}
    return render_template('course.html',course=course,done=done)

@app.route('/courses/<slug>/practice')
@login_required
def course_practice(slug):
    course=Course.query.filter_by(slug=slug).first_or_404()
    enforce_course_access(course)
    content=PRACTICE.get(slug, {'exercises': [], 'projects': []})
    return render_template('practice.html', course=course, exercises=content['exercises'], projects=content['projects'])

@app.route('/lessons/<int:lesson_id>')
@login_required
def lesson_detail(lesson_id):
    lesson=Lesson.query.get_or_404(lesson_id); course=lesson.course
    if course is None: abort(404)
    enforce_course_access(course)
    done=Progress.query.filter_by(user_id=current_user.id,lesson_id=lesson.id).first() is not None
    # Supplemental examples are selected by topic title, so the new beginner
    # sequence and the reordered legacy lessons each receive relevant examples.
    examples = extra_examples(course.slug,lesson.position,lesson.title)
    examples=[{**item,'walkthrough':code_walkthrough(item['code'],course.language),'expected':expected_behaviour(item,course.language)} for item in examples]
    main_example={'title':'Main lesson example','code':lesson.example}
    main_walkthrough=code_walkthrough(lesson.example,course.language)
    main_expected=expected_behaviour(main_example,course.language)
    bookmarked=LessonBookmark.query.filter_by(user_id=current_user.id,lesson_id=lesson.id).first() is not None
    note=LessonNote.query.filter_by(user_id=current_user.id,lesson_id=lesson.id).first()
    return render_template('lesson.html',lesson=lesson,course=course,done=done,extra_examples=examples,main_walkthrough=main_walkthrough,main_expected=main_expected,bookmarked=bookmarked,note=note,deep_dive=deep_dive(course.slug,lesson.position,lesson.title))

@app.post('/api/lessons/<int:lesson_id>/complete')
@login_required
def complete_lesson(lesson_id):
    lesson=Lesson.query.get_or_404(lesson_id)
    enforce_course_access(lesson.course)
    if not Progress.query.filter_by(user_id=current_user.id,lesson_id=lesson.id).first(): db.session.add(Progress(user_id=current_user.id,lesson_id=lesson.id)); db.session.commit()
    return jsonify(ok=True)

@app.post('/api/lessons/<int:lesson_id>/bookmark')
@login_required
def toggle_bookmark(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    enforce_course_access(lesson.course)
    item=LessonBookmark.query.filter_by(user_id=current_user.id,lesson_id=lesson_id).first()
    if item:
        db.session.delete(item); saved=False
    else:
        db.session.add(LessonBookmark(user_id=current_user.id,lesson_id=lesson_id)); saved=True
    db.session.commit()
    return jsonify(ok=True,saved=saved)

@app.route('/bookmarks')
@login_required
def bookmarks():
    query = LessonBookmark.query.filter_by(user_id=current_user.id).join(Lesson, LessonBookmark.lesson_id == Lesson.id).join(Course)
    if not can_access_advanced_courses():
        query = query.filter(Course.access_level == 'free')
    items=query.order_by(LessonBookmark.created_at.desc()).all()
    lessons=[db.session.get(Lesson,item.lesson_id) for item in items]
    return render_template('bookmarks.html',lessons=lessons)

@app.post('/api/lessons/<int:lesson_id>/notes')
@login_required
def save_lesson_note(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    enforce_course_access(lesson.course)
    data=request.get_json(silent=True) or {}; content=str(data.get('content',''))
    if len(content)>12000: return jsonify(error='Notes must be 12,000 characters or fewer.'),400
    note=LessonNote.query.filter_by(user_id=current_user.id,lesson_id=lesson_id).first()
    if not note: note=LessonNote(user_id=current_user.id,lesson_id=lesson_id); db.session.add(note)
    note.content=content; note.updated_at=datetime.utcnow(); db.session.commit()
    return jsonify(ok=True,updated_at=note.updated_at.isoformat())

@app.route('/search')
@login_required
def search():
    term=request.args.get('q','').strip()[:100]
    courses=[]; lessons=[]
    if term:
        like=f'%{term}%'
        course_query = Course.query.filter((Course.title.ilike(like))|(Course.description.ilike(like))|(Course.language.ilike(like)))
        lesson_query = Lesson.query.join(Course).filter((Lesson.title.ilike(like))|(Lesson.body.ilike(like)))
        if not can_access_advanced_courses():
            course_query = course_query.filter(Course.access_level == 'free')
            lesson_query = lesson_query.filter(Course.access_level == 'free')
        courses=course_query.limit(20).all()
        lessons=lesson_query.limit(40).all()
    return render_template('search.html',term=term,courses=courses,lessons=lessons)

@app.route('/community',methods=['GET','POST'])
@login_required
def community():
    denied = ensure_community_access()
    if denied:
        return denied
    if request.method == 'POST':
        title=request.form.get('title','').strip(); body=request.form.get('body','').strip()
        if not 5<=len(title)<=140 or not 10<=len(body)<=5000:
            flash('Use a title of 5–140 characters and a message of 10–5,000 characters.','error')
        else:
            db.session.add(ForumPost(user_id=current_user.id,title=title,body=body)); db.session.commit(); flash('Your discussion was posted.','success'); return redirect(url_for('community'))
    posts=ForumPost.query.order_by(ForumPost.created_at.desc()).limit(100).all()
    posts=[post for post in posts if post.user_id == current_user.id or not are_users_mutually_blocked(post.user_id)]
    blocked_users=CommunityUserBlock.query.filter_by(blocker_id=current_user.id).order_by(CommunityUserBlock.created_at.desc()).all()
    return render_template('community.html',posts=posts,blocked_users=blocked_users)

@app.route('/community/<int:post_id>',methods=['GET','POST'])
@login_required
def community_post(post_id):
    denied = ensure_community_access()
    if denied:
        return denied
    post=ForumPost.query.get_or_404(post_id)
    if post.user_id != current_user.id and are_users_mutually_blocked(post.user_id):
        abort(404)
    if request.method=='POST':
        body=request.form.get('body','').strip()
        if not 2<=len(body)<=3000: flash('Replies must be 2–3,000 characters.','error')
        else:
            db.session.add(ForumReply(post_id=post.id,user_id=current_user.id,body=body))
            if post.user_id != current_user.id:
                db.session.add(Notification(user_id=post.user_id,title='New discussion reply',body=f'{current_user.username} replied to “{post.title}”.'))
            db.session.commit(); return redirect(url_for('community_post',post_id=post.id))
    replies=ForumReply.query.filter_by(post_id=post.id).order_by(ForumReply.created_at.asc()).all()
    replies=[reply for reply in replies if reply.user_id == current_user.id or not are_users_mutually_blocked(reply.user_id)]
    return render_template('community_post.html',post=post,replies=replies)

@app.post('/community/report/<content_type>/<int:content_id>')
@login_required
def community_report(content_type, content_id):
    denied = ensure_community_access()
    if denied:
        return denied
    if content_type == 'post':
        item = ForumPost.query.get_or_404(content_id); reported_user_id = item.user_id; post_id=item.id; reply_id=None
    elif content_type == 'reply':
        item = ForumReply.query.get_or_404(content_id); reported_user_id = item.user_id; post_id=item.post_id; reply_id=item.id
    else:
        abort(404)
    if reported_user_id == current_user.id:
        flash('You cannot report your own content.','error')
        return redirect(url_for('community'))
    reason=request.form.get('reason','').strip()
    allowed={'Harassment or bullying','Spam or scams','Inappropriate content','Hate or discrimination','Other'}
    if reason not in allowed:
        abort(400)
    already=CommunityReport.query.filter_by(reporter_id=current_user.id,post_id=post_id,reply_id=reply_id,status='Open').first()
    if not already:
        db.session.add(CommunityReport(reporter_id=current_user.id,reported_user_id=reported_user_id,post_id=post_id,reply_id=reply_id,reason=reason,details=request.form.get('details','').strip()[:1000]))
        db.session.commit()
        flash('Thank you. Your report has been sent to the administrator.','success')
    else:
        flash('You have already reported this content.','info')
    return redirect(url_for('community_post',post_id=post_id))

@app.post('/community/block/<int:user_id>')
@login_required
def community_block_user(user_id):
    denied = ensure_community_access()
    if denied:
        return denied
    if user_id == current_user.id:
        abort(400)
    User.query.get_or_404(user_id)
    if not CommunityUserBlock.query.filter_by(blocker_id=current_user.id,blocked_id=user_id).first():
        db.session.add(CommunityUserBlock(blocker_id=current_user.id,blocked_id=user_id)); db.session.commit()
    flash('Community posts and replies are now hidden from both you and that learner.','success')
    return redirect(request.referrer or url_for('community'))

@app.post('/community/unblock/<int:user_id>')
@login_required
def community_unblock_user(user_id):
    denied = ensure_community_access()
    if denied:
        return denied
    CommunityUserBlock.query.filter_by(blocker_id=current_user.id,blocked_id=user_id).delete()
    db.session.commit()
    flash('Learner unblocked. Community content is visible again unless the other learner has also blocked you.','success')
    return redirect(url_for('community'))

@app.route('/submit-project/<slug>',methods=['GET','POST'])
@login_required
def submit_project(slug):
    course=Course.query.filter_by(slug=slug).first_or_404()
    enforce_course_access(course)
    if request.method=='POST':
        title=request.form.get('title','').strip()[:120]; description=request.form.get('description','').strip()[:4000]; project_url=request.form.get('project_url','').strip()[:500]
        if not title or len(description)<20: flash('Add a project title and at least 20 characters describing your work.','error')
        elif project_url and not project_url.startswith(('https://','http://')): flash('Project links must begin with http:// or https://.','error')
        else:
            db.session.add(ProjectSubmission(user_id=current_user.id,course_slug=slug,title=title,description=description,project_url=project_url)); db.session.commit(); flash('Project added to your portfolio.','success'); return redirect(url_for('dashboard'))
    return render_template('submit_project.html',course=course)

@app.route('/portfolio')
@login_required
def portfolio():
    submissions=ProjectSubmission.query.filter_by(user_id=current_user.id).order_by(ProjectSubmission.created_at.desc()).all()
    return render_template('portfolio.html',submissions=submissions)

@app.route('/achievements')
@login_required
def achievements():
    completed=Progress.query.filter_by(user_id=current_user.id).count(); projects=Project.query.filter_by(user_id=current_user.id).count(); attempts=QuizResult.query.filter_by(user_id=current_user.id).all()
    high_scores=sum(1 for r in attempts if r.total and r.score/r.total>=.8)
    badges=[('First steps','Complete your first lesson',completed>=1),('Consistent learner','Complete 10 lessons',completed>=10),('Course explorer','Complete 25 lessons',completed>=25),('Builder','Save your first code project',projects>=1),('Exam ready','Score at least 80% in an assessment',high_scores>=1),('High achiever','Score at least 80% in three assessments',high_scores>=3)]
    return render_template('achievements.html',badges=badges,completed=completed,projects=projects,high_scores=high_scores)

@app.route('/certificate/<slug>', methods=['GET', 'POST'])
@login_required
def certificate(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    enforce_course_access(course)
    total = len(course.lessons)
    completed = Progress.query.filter_by(user_id=current_user.id).join(Lesson).filter(Lesson.course_id == course.id).count()
    results = QuizResult.query.filter_by(user_id=current_user.id, course_slug=slug).all()
    best = max((round(r.score / r.total * 100) for r in results if r.total), default=0)
    eligible = total > 0 and completed == total and best >= 80
    payment = CertificatePayment.query.filter_by(user_id=current_user.id, course_slug=slug, status='paid').order_by(CertificatePayment.paid_at.desc()).first()
    paid = payment is not None

    if request.method == 'POST':
        certificate_name = request.form.get('certificate_name', '').strip()
        if not certificate_name or len(certificate_name) > 80:
            flash('Enter the name to print on your certificate (1–80 characters).', 'error')
            return redirect(url_for('certificate', slug=slug))

        # The learner may correct the certificate name without changing their account name.
        if request.form.get('action') == 'save_name':
            if not eligible and not paid:
                flash('Complete the course requirements before setting your certificate name.', 'error')
                return redirect(url_for('certificate', slug=slug))
            if payment:
                payment.certificate_name = certificate_name
            else:
                pending = CertificatePayment.query.filter_by(user_id=current_user.id, course_slug=slug).order_by(CertificatePayment.created_at.desc()).first()
                if pending:
                    pending.certificate_name = certificate_name
                else:
                    session[f'certificate_name_{slug}'] = certificate_name
            db.session.commit()
            flash('Certificate name saved.', 'success')
            return redirect(url_for('certificate', slug=slug))

        if not eligible:
            flash('Complete every lesson and score at least 80% in the final exam before collecting a certificate.', 'error')
            return redirect(url_for('certificate', slug=slug))
        if paid:
            payment.certificate_name = certificate_name
            db.session.commit()
            return redirect(url_for('certificate', slug=slug))

        # Administrators receive their own certificate without a Paystack charge.
        # Course completion and assessment requirements still apply.
        if is_admin_user():
            complimentary = CertificatePayment(
                user_id=current_user.id,
                course_slug=slug,
                reference='ADMIN-FREE-' + uuid.uuid4().hex,
                amount_kobo=0,
                status='paid',
                certificate_name=certificate_name,
                paid_at=datetime.utcnow()
            )
            db.session.add(complimentary)
            db.session.commit()
            flash('Your administrator certificate has been issued at no charge.', 'success')
            return redirect(url_for('certificate', slug=slug))

        secret = app.config['PAYSTACK_SECRET_KEY']
        fee = app.config['CERTIFICATE_FEE_NAIRA']
        if not secret:
            flash('Certificate payments are not enabled yet. The administrator must configure PAYSTACK_SECRET_KEY.', 'error')
            return redirect(url_for('certificate', slug=slug))
        reference = 'CC-' + uuid.uuid4().hex
        payment = CertificatePayment(user_id=current_user.id, course_slug=slug, reference=reference, amount_kobo=fee * 100, status='pending', certificate_name=certificate_name)
        db.session.add(payment)
        db.session.commit()
        payload = json.dumps({'email': current_user.email, 'amount': payment.amount_kobo, 'reference': reference, 'callback_url': url_for('verify_certificate_payment', _external=True), 'metadata': {'user_id': current_user.id, 'course_slug': slug, 'purpose': 'course_certificate'}}).encode()
        req = urllib.request.Request('https://api.paystack.co/transaction/initialize', data=payload, headers={'Authorization': 'Bearer ' + secret, 'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                data = json.loads(response.read().decode())
            if not data.get('status') or not data.get('data', {}).get('authorization_url'):
                raise ValueError('Payment provider did not return a checkout link.')
            return redirect(data['data']['authorization_url'])
        except Exception:
            app.logger.exception('Paystack initialization failed')
            payment.status = 'failed'
            db.session.commit()
            flash('Could not start payment. Please try again later.', 'error')
            return redirect(url_for('certificate', slug=slug))

    display_name = (payment.certificate_name if payment and payment.certificate_name else session.get(f'certificate_name_{slug}') or current_user.username)
    return render_template('certificate.html', course=course, eligible=eligible, completed=completed, total=total, best=best, paid=paid, is_admin=is_admin_user(), fee=app.config['CERTIFICATE_FEE_NAIRA'], certificate_name=display_name, learner=current_user, payment=payment, issued_date=(payment.paid_at if payment else None), admin_view=False)

@app.get('/certificate-payment/verify')
@login_required
def verify_certificate_payment():
    reference = request.args.get('reference', '').strip()
    payment = CertificatePayment.query.filter_by(reference=reference, user_id=current_user.id).first()
    if not payment:
        flash('Payment reference was not recognised.', 'error')
        return redirect(url_for('dashboard'))
    if payment.status != 'paid':
        secret = app.config['PAYSTACK_SECRET_KEY']
        if not secret:
            flash('Payment verification is unavailable. Contact the administrator.', 'error')
            return redirect(url_for('certificate', slug=payment.course_slug))
        req = urllib.request.Request('https://api.paystack.co/transaction/verify/' + reference, headers={'Authorization': 'Bearer ' + secret}, method='GET')
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                data = json.loads(response.read().decode())
            details = data.get('data', {})
            if data.get('status') and details.get('status') == 'success' and int(details.get('amount', -1)) == payment.amount_kobo and details.get('reference') == payment.reference:
                payment.status = 'paid'
                payment.paid_at = datetime.utcnow()
                db.session.commit()
            else:
                payment.status = 'failed'
                db.session.commit()
                flash('Payment could not be verified. No certificate has been issued.', 'error')
        except Exception:
            app.logger.exception('Paystack verification failed')
            flash('We could not verify the payment yet. Please contact support before trying again.', 'error')
    return redirect(url_for('certificate', slug=payment.course_slug))

@app.get('/admin/certificates')
@login_required
def admin_certificates():
    if not is_admin_user():
        abort(403)
    records = CertificatePayment.query.filter_by(status='paid').order_by(CertificatePayment.paid_at.desc()).all()
    return render_template('admin_certificates.html', certificates=records)

@app.get('/admin/certificates/<int:payment_id>')
@login_required
def admin_view_certificate(payment_id):
    if not is_admin_user():
        abort(403)
    payment = CertificatePayment.query.filter_by(id=payment_id, status='paid').first_or_404()
    course = Course.query.filter_by(slug=payment.course_slug).first_or_404()
    learner = User.query.get_or_404(payment.user_id)
    return render_template('certificate.html', course=course, eligible=True, completed=len(course.lessons), total=len(course.lessons), best=0, paid=True, fee=0, certificate_name=payment.certificate_name or learner.username, learner=learner, payment=payment, issued_date=payment.paid_at, admin_view=True)

@app.route('/monetization', methods=['GET'])
@login_required
def monetization_plan():
    # Older accounts are assigned a free-plan record the first time this page is opened.
    if not MembershipPayment.query.filter_by(user_id=current_user.id).first():
        db.session.add(MembershipPayment(user_id=current_user.id, plan='free', amount_kobo=0, status='active', starts_at=datetime.utcnow()))
        db.session.commit()
    now = datetime.utcnow()
    current_plan = MembershipPayment.query.filter(
        MembershipPayment.user_id == current_user.id,
        MembershipPayment.status.in_(['active', 'paid']),
        db.or_(MembershipPayment.plan == 'free', MembershipPayment.ends_at > now)
    ).order_by(MembershipPayment.created_at.desc()).first()
    if current_plan is None:
        # Expired paid access falls back to the free plan; transaction history is retained.
        MembershipPayment.query.filter(
            MembershipPayment.user_id == current_user.id,
            MembershipPayment.plan.in_(['monthly', 'annual']),
            MembershipPayment.status == 'paid',
            MembershipPayment.ends_at <= now
        ).update({'status': 'expired'})
        current_plan = MembershipPayment(user_id=current_user.id, plan='free', amount_kobo=0, status='active', starts_at=now)
        db.session.add(current_plan)
        db.session.commit()
    return render_template('monetization.html', fee=app.config['CERTIFICATE_FEE_NAIRA'], monthly_fee=app.config['MEMBERSHIP_MONTHLY_NAIRA'], annual_fee=app.config['MEMBERSHIP_ANNUAL_NAIRA'], current_plan=current_plan, payments_enabled=bool(app.config['PAYSTACK_SECRET_KEY']))

@app.post('/membership/subscribe')
@login_required
def membership_subscribe():
    plan = request.form.get('plan', '').strip()
    prices = {'monthly': app.config['MEMBERSHIP_MONTHLY_NAIRA'], 'annual': app.config['MEMBERSHIP_ANNUAL_NAIRA']}
    if plan not in prices:
        abort(400)
    secret = app.config['PAYSTACK_SECRET_KEY']
    if not secret:
        flash('Membership checkout is not enabled yet. The administrator must configure PAYSTACK_SECRET_KEY.', 'error')
        return redirect(url_for('monetization_plan'))
    reference = 'CC-MEM-' + uuid.uuid4().hex
    payment = MembershipPayment(user_id=current_user.id, plan=plan, reference=reference, amount_kobo=prices[plan] * 100, status='pending')
    db.session.add(payment)
    db.session.commit()
    payload = json.dumps({'email': current_user.email, 'amount': payment.amount_kobo, 'reference': reference, 'callback_url': url_for('verify_membership_payment', _external=True), 'metadata': {'user_id': current_user.id, 'plan': plan, 'purpose': 'membership'}}).encode()
    req = urllib.request.Request('https://api.paystack.co/transaction/initialize', data=payload, headers={'Authorization': 'Bearer ' + secret, 'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            data = json.loads(response.read().decode())
        if not data.get('status') or not data.get('data', {}).get('authorization_url'):
            raise ValueError('Payment provider did not return a checkout link.')
        return redirect(data['data']['authorization_url'])
    except Exception:
        app.logger.exception('Membership payment initialization failed')
        payment.status = 'failed'
        db.session.commit()
        flash('Could not start membership payment. Please try again later.', 'error')
        return redirect(url_for('monetization_plan'))

@app.get('/membership-payment/verify')
@login_required
def verify_membership_payment():
    reference = request.args.get('reference', '').strip()
    payment = MembershipPayment.query.filter_by(reference=reference, user_id=current_user.id).first()
    if not payment:
        flash('Membership payment reference was not recognised.', 'error')
        return redirect(url_for('monetization_plan'))
    if payment.status != 'paid':
        secret = app.config['PAYSTACK_SECRET_KEY']
        if not secret:
            flash('Payment verification is unavailable. Contact the administrator.', 'error')
            return redirect(url_for('monetization_plan'))
        req = urllib.request.Request('https://api.paystack.co/transaction/verify/' + reference, headers={'Authorization': 'Bearer ' + secret}, method='GET')
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                data = json.loads(response.read().decode())
            details = data.get('data', {})
            if data.get('status') and details.get('status') == 'success' and int(details.get('amount', -1)) == payment.amount_kobo and details.get('reference') == payment.reference:
                now = datetime.utcnow()
                # Keep the transaction history; deactivate any older active plan.
                MembershipPayment.query.filter_by(user_id=current_user.id, status='active').update({'status': 'superseded'})
                payment.status = 'paid'
                payment.paid_at = now
                payment.starts_at = now
                payment.ends_at = now + (timedelta(days=30) if payment.plan == 'monthly' else timedelta(days=365))
                db.session.commit()
                flash('Your membership payment was verified. Your plan is now active.', 'success')
            else:
                payment.status = 'failed'
                db.session.commit()
                flash('Payment could not be verified. Your membership has not been activated.', 'error')
        except Exception:
            app.logger.exception('Membership payment verification failed')
            flash('We could not verify the payment yet. Please contact support before trying again.', 'error')
    return redirect(url_for('monetization_plan'))

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if request.method=='POST':
        username=request.form.get('username','').strip()
        if not 3<=len(username)<=32 or not username.replace('_','').isalnum(): flash('Use 3–32 letters, numbers or underscores.','error')
        elif User.query.filter(User.username==username,User.id!=current_user.id).first(): flash('That username is already in use.','error')
        else: current_user.username=username; db.session.commit(); flash('Profile updated.','success'); return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/notifications')
@login_required
def notifications():
    items=Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(100).all()
    return render_template('notifications.html',items=items)

@app.post('/notifications/<int:notification_id>/read')
@login_required
def mark_notification_read(notification_id):
    item=Notification.query.filter_by(id=notification_id,user_id=current_user.id).first_or_404(); item.is_read=True; db.session.commit()
    return redirect(url_for('notifications'))

@app.route('/suggestions', methods=['GET', 'POST'])
@login_required
def suggestions():
    if request.method == 'POST':
        category = request.form.get('category', 'General').strip()[:40]
        title = request.form.get('title', '').strip()
        body = request.form.get('body', '').strip()
        allowed_categories = {'General', 'New lesson', 'Bug report', 'Feature request', 'Design', 'Other'}
        if category not in allowed_categories:
            category = 'General'
        if not 5 <= len(title) <= 140 or not 15 <= len(body) <= 3000:
            flash('Use a title of 5–140 characters and a description of 15–3,000 characters.', 'error')
        else:
            db.session.add(Suggestion(user_id=current_user.id, category=category, title=title, body=body))
            db.session.commit()
            flash('Thank you. Your suggestion has been sent to the FelixForge Academy team.', 'success')
            return redirect(url_for('suggestions'))
    items = Suggestion.query.filter_by(user_id=current_user.id).order_by(Suggestion.created_at.desc()).limit(50).all()
    return render_template('suggestions.html', items=items)

@app.post('/admin/announcement')
@login_required
def admin_announcement():
    if not app.config.get('ADMIN_ENABLED') or current_user.email.lower()!=app.config.get('ADMIN_EMAIL', ''): abort(403)
    title=request.form.get('title','').strip()[:140]; body=request.form.get('body','').strip()[:1000]
    if not title or len(body)<5: flash('Enter an announcement title and a message of at least five characters.','error')
    else:
        for user in User.query.all(): db.session.add(Notification(user_id=user.id,title=title,body=body))
        db.session.commit(); flash('Announcement sent to learner notification inboxes.','success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not app.config.get('ADMIN_ENABLED') or current_user.email.lower()!=app.config.get('ADMIN_EMAIL', ''): abort(403)
    now = datetime.utcnow()
    active_since = now - timedelta(days=7)
    new_since = now - timedelta(days=30)
    admin_email = app.config.get('ADMIN_EMAIL', '')
    active_query = db.session.query(UserActivity.user_id).join(User, User.id == UserActivity.user_id).filter(UserActivity.last_seen_at >= active_since)
    if admin_email:
        active_query = active_query.filter(User.email != admin_email)
    active_users = active_query.distinct().count()
    learner_query = User.query
    if admin_email:
        learner_query = learner_query.filter(User.email != admin_email)
    new_users = learner_query.filter(User.created_at >= new_since).count()
    suggestions = Suggestion.query.order_by(Suggestion.created_at.desc()).limit(100).all()
    quiz_query = QuizResult.query.join(User, User.id == QuizResult.user_id)
    membership_query = MembershipPayment.query.join(User, User.id == MembershipPayment.user_id)
    if admin_email:
        quiz_query = quiz_query.filter(User.email != admin_email)
        membership_query = membership_query.filter(User.email != admin_email)
    quiz_activity = quiz_query.order_by(QuizResult.created_at.desc()).limit(150).all()
    membership_activity = membership_query.order_by(MembershipPayment.created_at.desc()).limit(150).all()
    current_membership_by_user = {}
    eligible_memberships = MembershipPayment.query.filter(
        MembershipPayment.status.in_(['active', 'paid']),
        db.or_(MembershipPayment.plan == 'free', MembershipPayment.ends_at > now)
    ).order_by(MembershipPayment.created_at.desc()).all()
    for record in eligible_memberships:
        if record.user_id not in current_membership_by_user:
            current_membership_by_user[record.user_id] = record
    free_plan_count = sum(1 for record in current_membership_by_user.values() if record.plan == 'free')
    paid_plan_count = sum(1 for record in current_membership_by_user.values() if record.plan in {'monthly', 'annual'})
    membership_revenue = db.session.query(db.func.coalesce(db.func.sum(MembershipPayment.amount_kobo), 0)).filter_by(status='paid').scalar() // 100
    paid_certificate_payments = CertificatePayment.query.filter_by(status='paid').order_by(CertificatePayment.paid_at.desc()).all()
    certificate_revenue = sum(item.amount_kobo for item in paid_certificate_payments) // 100
    community_reports = CommunityReport.query.filter_by(status='Open').order_by(CommunityReport.created_at.desc()).limit(100).all()
    community_restrictions = CommunityRestriction.query.order_by(CommunityRestriction.created_at.desc()).all()
    return render_template(
        'admin.html',
        users=User.query.order_by(User.created_at.desc()).limit(100).all(),
        community_manage_users=learner_query.order_by(User.created_at.desc()).all(),
        courses=Course.query.order_by(Course.title).all(),
        lesson_count=Lesson.query.count(),
        post_count=ForumPost.query.count(),
        total_users=learner_query.count(),
        active_users=active_users,
        new_users=new_users,
        completed_lessons=Progress.query.count(),
        quiz_attempts=QuizResult.query.count(),
        project_submissions=ProjectSubmission.query.count(),
        suggestion_count=Suggestion.query.count(),
        certificate_sales=len(paid_certificate_payments),
        certificate_revenue=certificate_revenue,
        paid_certificates=paid_certificate_payments[:100],
        membership_revenue=membership_revenue,
        free_plan_count=free_plan_count,
        paid_plan_count=paid_plan_count,
        quiz_activity=quiz_activity,
        membership_activity=membership_activity,
        suggestions=suggestions,
        community_reports=community_reports,
        community_restrictions=community_restrictions,
    )

@app.post('/admin/community/block/<int:user_id>')
@login_required
def admin_block_community_user(user_id):
    if not is_admin_user(): abort(403)
    user=User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot restrict your own administrator account.','error')
        return redirect(url_for('admin_dashboard'))
    reason=request.form.get('reason','').strip()[:500]
    restriction=CommunityRestriction.query.filter_by(user_id=user.id).first()
    if restriction:
        restriction.reason=reason
        restriction.admin_id=current_user.id
    else:
        db.session.add(CommunityRestriction(user_id=user.id,admin_id=current_user.id,reason=reason))
    db.session.add(Notification(user_id=user.id,title='Community access restricted',body='An administrator has restricted your access to the community area. You can still use the other learning features.' + (f' Reason: {reason}' if reason else '')))
    db.session.commit()
    flash(f'{user.username} can no longer access the community.','success')
    return redirect(url_for('admin_dashboard'))

@app.post('/admin/community/unblock/<int:user_id>')
@login_required
def admin_unblock_community_user(user_id):
    if not is_admin_user(): abort(403)
    restriction=CommunityRestriction.query.filter_by(user_id=user_id).first_or_404()
    db.session.delete(restriction)
    db.session.add(Notification(user_id=user_id,title='Community access restored',body='An administrator has restored your access to the community.'))
    db.session.commit()
    flash('Community access restored.','success')
    return redirect(url_for('admin_dashboard'))

@app.post('/admin/community/report/<int:report_id>')
@login_required
def admin_resolve_community_report(report_id):
    if not is_admin_user(): abort(403)
    report=CommunityReport.query.get_or_404(report_id)
    action=request.form.get('action')
    if action not in {'Reviewed','Dismissed'}: abort(400)
    report.status=action
    db.session.commit()
    flash(f'Report marked {action.lower()}.','success')
    return redirect(url_for('admin_dashboard'))

@app.post('/admin/suggestions/<int:suggestion_id>')
@login_required
def admin_update_suggestion(suggestion_id):
    if not app.config.get('ADMIN_ENABLED') or current_user.email.lower()!=app.config.get('ADMIN_EMAIL', ''): abort(403)
    item = Suggestion.query.get_or_404(suggestion_id)
    status = request.form.get('status', 'New')
    if status not in {'New', 'Under review', 'Planned', 'Implemented', 'Declined'}:
        abort(400)
    new_note = request.form.get('admin_note', '').strip()[:1000]
    changed = item.status != status or item.admin_note != new_note
    item.status = status
    item.admin_note = new_note
    item.updated_at = datetime.utcnow()
    if changed:
        notice = f'Your suggestion “{item.title}” is now marked: {status}.'
        if new_note:
            notice += f' Administrator response: {new_note}'
        db.session.add(Notification(user_id=item.user_id, title='Suggestion update', body=notice[:1000]))
    db.session.commit()
    flash('Suggestion status updated.', 'success')
    return redirect(url_for('admin_dashboard'))

@app.post('/admin/lessons/<int:lesson_id>')
@login_required
def admin_edit_lesson(lesson_id):
    if not app.config.get('ADMIN_ENABLED') or current_user.email.lower()!=app.config.get('ADMIN_EMAIL', ''): abort(403)
    lesson=Lesson.query.get_or_404(lesson_id); title=request.form.get('title','').strip(); body=request.form.get('body','').strip(); example=request.form.get('example','')
    if not title or not body or len(body)>30000 or len(example)>12000: flash('Lesson fields are invalid or too long.','error')
    else: lesson.title=title[:120]; lesson.body=body; lesson.example=example; db.session.commit(); flash('Lesson updated.','success')
    return redirect(url_for('admin_dashboard'))

@app.route('/editor')
@login_required
def editor():
    projects=Project.query.filter_by(user_id=current_user.id).order_by(Project.updated_at.desc()).all(); selected=projects[0] if projects else None
    return render_template('editor.html',projects=projects,selected=selected)

@app.get('/api/projects')
@login_required
def list_projects():
    return jsonify([{'id':p.id,'name':p.name,'language':p.language,'updated_at':p.updated_at.isoformat()} for p in Project.query.filter_by(user_id=current_user.id).order_by(Project.updated_at.desc()).all()])

@app.post('/api/projects')
@login_required
def save_project():
    data=request.get_json(silent=True) or {}; name=str(data.get('name','Untitled project')).strip()[:80] or 'Untitled project'; language=str(data.get('language','python')).lower(); files=data.get('files',{})
    if language not in EDITOR_LANGUAGES or not isinstance(files,dict) or len(files)>20: return jsonify(error='Invalid project data.'),400
    safe_files={}
    for filename,content in files.items():
        filename=str(filename)
        if len(filename)>80 or '/' in filename or '\\' in filename or filename.startswith('.'): return jsonify(error='Invalid file name.'),400
        if not isinstance(content,str) or len(content)>100000: return jsonify(error='File is too large.'),400
        safe_files[filename]=content
    pid=data.get('id'); project=db.session.get(Project,int(pid)) if str(pid or '').isdigit() else None
    if project and project.user_id!=current_user.id: abort(404)
    if not project: project=Project(user_id=current_user.id); db.session.add(project)
    project.name=name; project.language=language; project.files_json=json.dumps(safe_files); project.updated_at=datetime.utcnow(); db.session.commit()
    return jsonify(ok=True,id=project.id,name=project.name,updated_at=project.updated_at.isoformat())

@app.get('/api/projects/<int:project_id>')
@login_required
def get_project(project_id):
    p=Project.query.filter_by(id=project_id,user_id=current_user.id).first_or_404()
    return jsonify(id=p.id,name=p.name,language=p.language,files=json.loads(p.files_json))

EDITOR_LANGUAGES={'python','javascript','typescript','html','css','c','cpp','java','csharp','php','sql','go','rust','ruby','swift','kotlin','json'}

ALLOWED_LANGUAGES={
 'python':{'image':'python:3.12-alpine','file':'main.py','cmd':['python','/workspace/main.py']},
 'javascript':{'image':'node:22-alpine','file':'main.js','cmd':['node','/workspace/main.js']},
  'php':{'image':'php:8.3-cli-alpine','file':'main.php','cmd':['php','/workspace/main.php']},
 'ruby':{'image':'ruby:3.3-alpine','file':'main.rb','cmd':['ruby','/workspace/main.rb']},
 'go':{'image':'golang:1.23-alpine','file':'main.go','cmd':['sh','-lc','GOCACHE=/tmp/go-cache go run /workspace/main.go']},
 'c':{'image':'gcc:14','file':'main.c','cmd':['sh','-lc','gcc /workspace/main.c -o /tmp/program && /tmp/program']},
 'cpp':{'image':'gcc:14','file':'main.cpp','cmd':['sh','-lc','g++ /workspace/main.cpp -std=c++17 -O0 -o /tmp/program && /tmp/program']},
 'java':{'image':'eclipse-temurin:21-jdk','file':'Main.java','cmd':['sh','-lc','javac -d /tmp /workspace/Main.java && java -cp /tmp Main']},
}
@app.post('/api/run')
@login_required
def run_code():
    data=request.get_json(silent=True) or {}; language=str(data.get('language','')).lower(); source=data.get('code','')
    if language not in ALLOWED_LANGUAGES: return jsonify(error='This language is not enabled for server execution.'),400
    if not isinstance(source,str) or not source.strip() or len(source)>30000: return jsonify(error='Code must be between 1 and 30,000 characters.'),400
    if not os.environ.get('ENABLE_CODE_RUNNER','false').lower()=='true': return jsonify(error='Code execution is disabled. Follow README.md to configure the isolated Docker runner before enabling it.'),503
    cfg=ALLOWED_LANGUAGES[language]
    with tempfile.TemporaryDirectory(prefix='cc-run-') as tmp:
        host=pathlib.Path(tmp); os.chmod(host,0o755); source_path=host/cfg['file']; source_path.write_text(source,encoding='utf-8'); os.chmod(source_path,0o644)
        command=['docker','run','--rm','--network','none','--memory','128m','--cpus','0.5','--pids-limit','64','--read-only','--tmpfs','/tmp:rw,nosuid,size=24m','--cap-drop','ALL','--security-opt','no-new-privileges','--user','1000:1000','--mount',f'type=bind,src={host},dst=/workspace,readonly',cfg['image'],*cfg['cmd']]
        try:
            proc=subprocess.run(command,capture_output=True,text=True,timeout=8,check=False)
            return jsonify(stdout=proc.stdout[-12000:],stderr=proc.stderr[-6000:],exit_code=proc.returncode)
        except subprocess.TimeoutExpired: return jsonify(error='Execution stopped: the 8-second time limit was reached.'),408
        except FileNotFoundError: return jsonify(error='Docker is not installed or is not available on the server.'),503
        except Exception: app.logger.exception('Runner error'); return jsonify(error='The code runner encountered an internal error.'),500

@app.get('/api/quiz/<slug>')
@login_required
def get_quiz(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    enforce_course_access(course)
    questions=QuizQuestion.query.filter_by(course_slug=slug).order_by(QuizQuestion.position).all()
    return jsonify(questions=[{'id':q.id,'prompt':q.prompt,'options':json.loads(q.options_json)} for q in questions])

@app.post('/api/quiz/<slug>')
@login_required
def save_quiz(slug):
    course = Course.query.filter_by(slug=slug).first_or_404()
    enforce_course_access(course)
    data=request.get_json(silent=True) or {}; answers=data.get('answers',{})
    questions=QuizQuestion.query.filter_by(course_slug=slug).order_by(QuizQuestion.position).all()
    if not questions or not isinstance(answers,dict): return jsonify(error='No quiz is available for this course.'),400
    score=0; feedback=[]
    for q in questions:
        raw=answers.get(str(q.id)); correct=isinstance(raw,int) and raw==q.correct_index
        score += int(correct)
        feedback.append({'question':q.prompt,'correct':correct,'correct_answer':json.loads(q.options_json)[q.correct_index],'explanation':q.explanation})
    db.session.add(QuizResult(user_id=current_user.id,course_slug=slug,score=score,total=len(questions))); db.session.commit()
    return jsonify(ok=True,score=score,total=len(questions),feedback=feedback)

@app.post('/api/ai-tutor')
@login_required
def ai_tutor():
    data=request.get_json(silent=True) or {}; question=str(data.get('question','')).strip()[:3000]; code=str(data.get('code',''))[:12000]; language=str(data.get('language','')).lower()
    api_url=os.environ.get('AI_API_URL','').strip(); api_key=os.environ.get('AI_API_KEY','').strip(); model=os.environ.get('AI_MODEL','')
    if not question: return jsonify(error='Enter a question first.'),400
    if not api_url or not api_key or not model: return jsonify(error='AI tutor is not configured yet. Add AI_API_URL, AI_API_KEY and AI_MODEL to your .env file.'),503
    try:
        import urllib.request
        payload={'model':model,'messages':[{'role':'system','content':'You are FelixForge Academy\'s programming tutor. Teach clearly, encourage learning, explain mistakes, and never claim code was executed unless it was. Do not ask for passwords, secrets or personal data.'},{'role':'user','content':f'Language: {language}\nQuestion: {question}\n\nCode (if supplied):\n{code}'}],'temperature':0.3}
        req=urllib.request.Request(api_url,data=json.dumps(payload).encode(),headers={'Authorization':f'Bearer {api_key}','Content-Type':'application/json'},method='POST')
        with urllib.request.urlopen(req,timeout=25) as response: result=json.loads(response.read().decode())
        answer=result.get('choices',[{}])[0].get('message',{}).get('content','No answer returned.')
        return jsonify(answer=str(answer)[:12000])
    except Exception: app.logger.exception('AI tutor request failed'); return jsonify(error='The AI tutor could not connect. Check your AI provider settings.'),502

@app.errorhandler(413)
def too_large(_): return jsonify(error='Request is too large.'),413

def ensure_admin_account():
    admin_email = app.config.get('ADMIN_EMAIL', '')
    admin_password = os.environ.get('ADMIN_PASSWORD', '')
    if not admin_email or not admin_password:
        return
    if len(admin_password) < 16:
        raise RuntimeError('ADMIN_PASSWORD must contain at least 16 characters.')
    existing = User.query.filter_by(email=admin_email).first()
    if existing:
        # Keep the configured secret authoritative so an old unverified account
        # cannot silently become the administrator just because its email matches.
        if not existing.check_password(admin_password):
            existing.set_password(admin_password)
            db.session.commit()
        return
    username = app.config.get('ADMIN_USERNAME', 'admin')[:32]
    if not 3 <= len(username) <= 32 or not username.replace('_', '').isalnum():
        raise RuntimeError('ADMIN_USERNAME must be 3–32 letters, numbers or underscores.')
    if User.query.filter_by(username=username).first():
        username = f"admin_{uuid.uuid4().hex[:8]}"
    administrator = User(username=username, email=admin_email)
    administrator.set_password(admin_password)
    db.session.add(administrator)
    db.session.commit()

with app.app_context():
    db.create_all()
    # db.create_all() does not add columns to existing tables; migrate this
    # single additive column safely without deleting learner data.
    from sqlalchemy import inspect, text
    course_columns = {column['name'] for column in inspect(db.engine).get_columns('course')}
    if 'access_level' not in course_columns:
        with db.engine.begin() as connection:
            connection.execute(text("ALTER TABLE course ADD COLUMN access_level VARCHAR(20) NOT NULL DEFAULT 'free'"))
    certificate_columns = {column['name'] for column in inspect(db.engine).get_columns('certificate_payment')}
    if 'certificate_name' not in certificate_columns:
        with db.engine.begin() as connection:
            connection.execute(text('ALTER TABLE certificate_payment ADD COLUMN certificate_name VARCHAR(80)'))
    ensure_admin_account()
    seed_database()
    seed_advanced_courses()

if __name__=='__main__': app.run(host='127.0.0.1',port=int(os.environ.get('PORT',5000)),debug=os.environ.get('FLASK_DEBUG')=='1')
