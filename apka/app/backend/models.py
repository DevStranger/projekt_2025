# Zamiast: from flask_sqlalchemy import SQLAlchemy
# Używamy istniejącego obiektu z init.py
from . import db  # <-- importujemy "db" z __init__.py

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), unique=True, nullable=False)
