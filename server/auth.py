from flask import Blueprint, request, session, jsonify, abort
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        abort(400, 'Email and password required')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        abort(401, 'Invalid email or password')

    session['user_id'] = user.id
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }), 200

@auth_bp.route('/logout', methods=['DELETE'])
def logout():
    session.pop('user_id', None)
    return '', 204

@auth_bp.route('/check_session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if not user_id:
        return '', 401

    user = User.query.get(user_id)
    if not user:
        return '', 401

    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }), 200
