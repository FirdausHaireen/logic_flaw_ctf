
from flask import Flask, request, session, redirect, render_template, url_for
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'admin': {'password': 'admin123'},
    'user': {'password': 'user123'}
}

reset_tokens = {}

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            session['user'] = username
            return redirect('/admin/dashboard' if username == 'admin' else '/')
    return render_template('index.html')

@app.route('/request-reset', methods=['GET', 'POST'])
def request_reset():
    token = None
    if request.method == 'POST':
        username = request.form['username']
        if username in users:
            token = os.urandom(8).hex()
            reset_tokens[username] = {'token': token, 'expires': datetime.now() + timedelta(minutes=10)}
    return render_template('request_reset.html', token=token)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')
    for user, info in reset_tokens.items():
        if info['token'] == token and info['expires'] > datetime.now():
            if request.method == 'POST':
                new_pass = request.form['password']
                users[user]['password'] = new_pass
                return f"Password for {user} has been reset."
            return render_template('reset_password.html')
    return "Invalid or expired token."

@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('user') == 'admin':
        with open('flag.txt') as f:
            flag = f.read()
        return render_template('admin.html', flag=flag)
    return "Unauthorized", 403

if __name__ == '__main__':
    app.run(debug=True)
