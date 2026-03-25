import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from database import db, User, History

from flask import Flask, request, redirect, jsonify, render_template
from agent.issue_parser import parse_issue
from agent.fix_generator import generate_fix
from agent.test_generator import generate_tests

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_secret_for_dev")

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(username=username).first():
            return render_template("signup.html", error="Username already exists.")
        if User.query.filter_by(email=email).first():
            return render_template("signup.html", error="Email already exists.")
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("signup.html", success="Account created! You can now log in.")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login_id = request.form.get("login_id")
        password = request.form.get("password")
        
        user = User.query.filter((User.username == login_id) | (User.email == login_id)).filter_by(password=password).first()
        
        if user:
            login_user(user)
            return redirect("/")
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    histories = History.query.filter_by(user_id=current_user.id).order_by(History.created_at.desc()).all()
    fix = ""
    tests = ""
    if request.method == "POST":
        issue = request.form.get("issue")
        parsed = parse_issue(issue)
        fix = generate_fix(parsed)
        tests = generate_tests(parsed)
        title = issue[:30] + "..." if len(issue) > 30 else issue
        new_chat = History(user_id=current_user.id, title=title, issue=issue, fix=fix, tests=tests)
        db.session.add(new_chat)
        db.session.commit()
        return redirect(f"/chat/{new_chat.id}")
    return render_template("dashboard.html", histories=histories, fix=fix, tests=tests)

@app.route("/chat/<int:chat_id>")
@login_required
def view_chat(chat_id):
    histories = History.query.filter_by(user_id=current_user.id).order_by(History.created_at.desc()).all()
    chat = History.query.filter_by(id=chat_id, user_id=current_user.id).first()
    if not chat:
        return redirect("/")
    return render_template("dashboard.html", histories=histories, current_chat=chat)

@app.route("/delete_chat/<int:chat_id>")
@login_required
def delete_chat(chat_id):
    chat = History.query.filter_by(id=chat_id, user_id=current_user.id).first()
    if chat:
        db.session.delete(chat)
        db.session.commit()
    return redirect("/")

@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/settings")
@login_required
def settings():
    return render_template("settings.html")

@app.route("/developer")
@login_required
def developer():
    return render_template("developer.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    if data.get("object_kind") == "issue":
        issue_title = data["object_attributes"]["title"]
        issue_desc = data["object_attributes"]["description"]
        issue_text = issue_title + " " + issue_desc
        parsed = parse_issue(issue_text)
        fix = generate_fix(parsed)
        tests = generate_tests(parsed)
        return jsonify({"status": "processed"})
    return jsonify({"status": "ignored"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
