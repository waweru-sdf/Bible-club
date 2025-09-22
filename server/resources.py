from flask import request
from flask_restful import Resource
from models import db, User, Session, UserSession, Reflection
from datetime import datetime

# ----------user----------
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [u.to_dict() for u in users], 200

    def post(self):
        data = request.get_json()
        user = User(name=data["name"], email=data["email"], password=data["password"])
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201

class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user.to_dict(), 200

    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        if "name" in data: user.name = data["name"]
        if "email" in data: user.email = data["email"]
        if "password" in data: user.password = data["password"]
        db.session.commit()
        return user.to_dict(), 200

    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted"}, 204