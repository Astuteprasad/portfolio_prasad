import json
import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, abort

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

# ── Load data ──────────────────────────────────────────────
def load_data():
    with open('data.json', 'r') as f:
        return json.load(f)

# ── Database setup ─────────────────────────────────────────
def get_db():
    db = sqlite3.connect('portfolio.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            email     TEXT NOT NULL,
            subject   TEXT NOT NULL,
            message   TEXT NOT NULL,
            created   TEXT NOT NULL
        )
    ''')
    db.commit()
    db.close()

init_db()

# ── Routes ─────────────────────────────────────────────────

@app.route('/')
def index():
    data = load_data()
    highlight_projects = [p for p in data['projects'] if p.get('highlight')][:3]
    return render_template('index.html',
                           personal=data['personal'],
                           skills=data['skills'],
                           projects=highlight_projects)

@app.route('/about')
def about():
    data = load_data()
    return render_template('about.html',
                           personal=data['personal'],
                           skills=data['skills'],
                           experience=data['experience'])

@app.route('/projects')
def projects():
    data = load_data()
    category = request.args.get('category', 'All')
    all_projects = data['projects']
    if category != 'All':
        filtered = [p for p in all_projects if p['category'] == category]
    else:
        filtered = all_projects
    categories = ['All', 'Credit Risk', 'Excel', 'Power BI', 'ML', 'Data']
    return render_template('projects.html',
                           projects=filtered,
                           categories=categories,
                           active_category=category,
                           personal=data['personal'])

@app.route('/projects/<project_id>')
def project_detail(project_id):
    data = load_data()
    project = next((p for p in data['projects'] if p['id'] == project_id), None)
    if not project:
        abort(404)
    return render_template('project_detail.html',
                           project=project,
                           personal=data['personal'])

@app.route('/experience')
def experience():
    data = load_data()
    return render_template('experience.html',
                           experience=data['experience'],
                           personal=data['personal'])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    data = load_data()
    if request.method == 'POST':
        name    = request.form.get('name', '').strip()
        email   = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        errors = []
        if not name:    errors.append('Name is required.')
        if not email or '@' not in email:
            errors.append('A valid email is required.')
        if not subject: errors.append('Subject is required.')
        if not message: errors.append('Message is required.')

        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            db = get_db()
            db.execute(
                'INSERT INTO messages (name, email, subject, message, created) VALUES (?,?,?,?,?)',
                (name, email, subject, message, datetime.now().isoformat())
            )
            db.commit()
            db.close()
            flash('Message sent! I will get back to you shortly.', 'success')
            return redirect(url_for('contact'))

    return render_template('contact.html', personal=data['personal'])

# ── Error handlers ─────────────────────────────────────────
@app.errorhandler(404)
def page_not_found(e):
    data = load_data()
    return render_template('404.html', personal=data['personal']), 404

@app.errorhandler(500)
def server_error(e):
    data = load_data()
    return render_template('404.html', personal=data['personal']), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)