from flask import Flask, request, session, jsonify, abort
import os
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
bcrypt = Bcrypt(app)


class User:
    _users = {
        'alice': {'id': 1, 'username': 'alice', 'email': 'alice@example.com', 'password_hash': bcrypt.generate_password_hash('password123').decode('utf-8')},
        'bob': {'id': 2, 'username': 'bob', 'email': 'bob@example.com', 'password_hash': bcrypt.generate_password_hash('password456').decode('utf-8')}
    }

    @classmethod
    def get_by_username_or_email(cls, identifier):
        # Check if identifier is username
        user = cls._users.get(identifier)
        if user:
            return user
        # Check if identifier is email
        for u in cls._users.values():
            if u.get('email') == identifier:
                return u
        return None

    @classmethod
    def get_by_id(cls, user_id):
        for user in cls._users.values():
            if user['id'] == user_id:
                return user
        return None

    @classmethod
    def check_password(cls, identifier, password):
        user = cls.get_by_username_or_email(identifier)
        if user and bcrypt.check_password_hash(user['password_hash'], password):
            return user
        return None

    @classmethod
    def create_user(cls, username, email, password):
        if username in cls._users:
            return None
        # Check if email already exists
        for u in cls._users.values():
            if u.get('email') == email:
                return None
        user_id = max([u['id'] for u in cls._users.values()]) + 1
        cls._users[username] = {
            'id': user_id,
            'username': username,
            'email': email,
            'password_hash': bcrypt.generate_password_hash(password).decode('utf-8')
        }
        return cls._users[username]

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if not username or not password:
        abort(400, 'Username and password are required')

    user = User.create_user(username, email, password)
    if not user:
        abort(409, 'Username already exists')

    session['user_id'] = user['id']
    return jsonify({'id': user['id'], 'username': user['username'], 'email': user.get('email')}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('username') or data.get('email')
    password = data.get('password')
    if not identifier or not password:
        abort(400, 'Username/email and password are required')

    user = User.check_password(identifier, password)
    if not user:
        abort(401, 'Invalid username/email or password')

    session['user_id'] = user['id']
    return jsonify({'id': user['id'], 'username': user['username'], 'email': user.get('email')}), 200

@app.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return '', 204

@app.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id is None:
        return '', 401

    user = User.get_by_id(user_id)
    if not user:
        return '', 401

    return jsonify({'id': user['id'], 'username': user['username'], 'email': user.get('email')}), 200
