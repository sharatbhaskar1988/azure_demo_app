from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Environment name (DEV by default)
ENV = os.getenv('ENVIRONMENT', 'DEV').upper()

# Use PostgreSQL from docker-compose, fallback to SQLite for local testing
DB_URL = os.getenv(
    'DB_URL',
    f"sqlite:///{ENV.lower()}_db.db"
)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# -------------------------
# Database Model
# -------------------------
class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Open')


# -------------------------
# Create tables at startup
# IMPORTANT:
# This works for gunicorn too.
# -------------------------
with app.app_context():
    db.create_all()


# -------------------------
# Routes
# -------------------------

@app.route('/')
def index():
    tickets = Ticket.query.all()
    return render_template(
        'index.html',
        tickets=tickets,
        env=ENV
    )


@app.route('/ticket/new', methods=['GET', 'POST'])
def new_ticket():

    if request.method == 'POST':

        title = request.form['title']

        ticket = Ticket(
            title=title
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect(
            url_for('index')
        )

    return render_template(
        'new_ticket.html',
        env=ENV
    )


@app.route('/health')
def health():
    return {
        'status': 'healthy',
        'environment': ENV
    }, 200


# -------------------------
# Local run only
# Docker uses gunicorn
# -------------------------
if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000
    )