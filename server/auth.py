from flask import request, jsonify
from flask_restful import Resource
from models import User
from extensions import db
from auth_utils import create_jwt  


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

        if User.query.filter_by(email=email).first():
            return {"message": "User already exists"}, 400

        user = User(name=name, email=email)
        user.set_password(password)  
        db.session.add(user)
        db.session.commit()

        token = create_jwt(user.id)
        return {"message": "User created successfully!", "token": token, "user": user.to_dict()}, 201


class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required"}, 400

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            token = create_jwt(user.id)
            return {"message": "Login successful!", "token": token, "user": user.to_dict()}, 200

        return {"message": "Invalid credentials"}, 401


