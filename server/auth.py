from flask_restful import Resource
from flask import request, jsonify
from werkzeug.security import check_password_hash
from models import User
from extensions import db

class Register(Resource):
    def get(self):
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])

    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
       

        if not username or not password:
            return {"Message": "Username and password are required"}, 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {"Message": "User already exists"}, 400

        new_user = User(username=username)
        new_user.set_password(password)  
        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully!"}, 201

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return {"message": "Username and password are required"}, 400

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):  
            return {"message": "Login successful!"}, 200
        else:
            return {"message": "Invalid credentials"}, 401