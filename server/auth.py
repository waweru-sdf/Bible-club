from flask_restful import Resource
from flask import request, jsonify
from models import User
from extensions import db


class Register(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return {"message": "Name, email, and password are required"}, 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists"}, 400

        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully!"}, 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return {"message": "Login successful!"}, 200
        else:
            return {"message": "Invalid credentials"}, 401
