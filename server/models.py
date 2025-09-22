from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bibleclub.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)  # initializes flask-migrate
CORS(app)  # Enables CORS for all routes


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(300), nullable=False)

    sessions_facilitated = db.relationship(
        'Session', back_populates='facilitator', cascade='all, delete-orphan')
    reflections = db.relationship(
        'Reflection', back_populates='user', cascade='all, delete-orphan')
    user_sessions = db.relationship(
        'UserSession', back_populates='user', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
       
    def create(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<User {self.id} {self.email}>'


class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    theme = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    facilitator_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

    facilitator = db.relationship('User', back_populates='sessions_facilitated')
    reflections = db.relationship('Reflection',
                                  back_populates='session',
                                  cascade='all, delete-orphan')
    session_memberships = db.relationship(
        'UserSession', back_populates='session', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'theme': self.theme,
            'date': self.date,
            'facilitator_id': self.facilitator_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Session {self.id} "{self.title}">'


class UserSession(db.Model, SerializerMixin):
    __tablename__ = 'user_sessions'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), index=True)

    user = db.relationship('User', back_populates='user_sessions')
    session = db.relationship('Session', back_populates='session_memberships')

    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'user_id': self.user_id,
            'session_id': self.session_id,
        }

    def __repr__(self):
        return f'<UserSession {self.id} User {self.user_id} Session {self.session_id}>'


class Reflection(db.Model, SerializerMixin):
    __tablename__ = 'reflections'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), index=True)

    user = db.relationship('User', back_populates='reflections')
    session = db.relationship('Session', back_populates='reflections')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return f'<Reflection {self.id} User {self.user_id} Session {self.session_id}>'


if __name__ == '__main__':
    app.run(debug=True, port=5005)
