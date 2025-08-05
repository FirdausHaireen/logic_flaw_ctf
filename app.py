
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(minutes=30)

users = {
    "alice": {"password": "alice123", "role": "employee"},
    "bob": {"password": "bob123", "role": "admin"}
}

pending_requests = []

@app.route("/")
def index():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"], role=session["role"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            session["user"] = username
            session["role"] = users[username]["role"]
            return redirect(url_for("index"))
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/request-access", methods=["GET", "POST"])
def request_access():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        user = session["user"]
        role = request.form["role"]
        pending_requests.append({"user": user, "role": role})
        return "Request submitted"
    return render_template("request_access.html", user=session["user"])

@app.route("/admin/pending", methods=["GET", "POST"])
def admin_panel():
    if "user" not in session or session.get("role") != "admin":
        return "Access denied"
    if request.method == "POST":
        user = request.form["user"]
        role = request.form["role"]
        if user in users:
            users[user]["role"] = role
    return render_template("admin_panel.html", requests=pending_requests)

@app.route("/admin/panel")
def super_admin():
    if "user" in session and session.get("role") == "admin":
        return "FLAG{privilege_escalation_success}"
    return "Access denied"
