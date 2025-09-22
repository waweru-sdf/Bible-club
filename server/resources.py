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
