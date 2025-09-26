from extensions import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


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

    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
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

   
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'theme': self.theme,
            'date': self.date.isoformat() if self.date else None,
            'facilitator_id': self.facilitator_id

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

  

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'session_id': self.session_id
           
        }

    def __repr__(self):
        return f'<Reflection {self.id} User {self.user_id} Session {self.session_id}>'
