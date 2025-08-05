
from flask import Flask, render_template, request, redirect, session, url_for
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.permanent_session_lifetime = timedelta(minutes=30)

users = {
    "alice": {"password": "alicepass", "orders": ["ORD-2394F3C1", "ORD-2394F3C2"]},
    "bob": {"password": "bobpass", "orders": ["ORD-2394F0C1"]}
}

orders = {
    "ORD-2394F0C1": {"user": "bob", "item": "DJI Air 3S", "total": "$999", "flag": "pkb{harder_idor_order_access}"},
    "ORD-2394F3C1": {"user": "alice", "item": "Phone Case", "total": "$12", "flag": None},
    "ORD-2394F3C2": {"user": "alice", "item": "Bluetooth Speaker", "total": "$45", "flag": None},
    "ORD-2394F3C3": {"user": "alice", "item": "Sony A7RV and Sony 70-200MM F2.8", "total": "$4500", "flag": "pkb{dGhpc2lzbm90dGhlZmxhZw==}"}
}

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["username"]
        pw = request.form["password"]
        if uname in users and users[uname]["password"] == pw:
            session["username"] = uname
            return redirect(url_for("dashboard"))
        else:
            return "Invalid login"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    username = session["username"]
    user_orders = users[username]["orders"]
    return render_template("dashboard.html", username=username, orders=user_orders)

@app.route("/orders/view/<order_id>")
def view_order(order_id):
    if "username" not in session:
        return redirect(url_for("login"))
    order = orders.get(order_id)
    if not order:
        return "Order not found", 404
    return render_template("order.html", order_id=order_id, order=order)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
