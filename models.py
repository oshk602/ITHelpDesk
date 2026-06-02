from extensions import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        default='user'
    )

    tickets = db.relationship(
        'Ticket',
        backref='author',
        lazy=True
    )

class Ticket(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default='Open'
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )