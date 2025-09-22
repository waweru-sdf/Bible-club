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
    


# ----------session----------
class SessionListResource(Resource):
    def get(self):
        sessions = Session.query.all()
        return [s.to_dict() for s in sessions], 200

    def post(self):
        data = request.get_json()
        session = Session(
            title=data["title"],
            theme=data["theme"],
            date=data["date"],
            facilitator_id=data["facilitator_id"]
        )
        db.session.add(session)
        db.session.commit()
        # automatically add facilitator as participant
        user_session = UserSession(user_id=data["facilitator_id"], session_id=session.id, role="facilitator")
        db.session.add(user_session)
        db.session.commit()
        return session.to_dict(), 201


class SessionResource(Resource):
    def get(self, id):
        session = Session.query.get_or_404(id)
        return session.to_dict(), 200

    def patch(self, id):
        session = Session.query.get_or_404(id)
        data = request.get_json()
        if "title" in data: session.title = data["title"]
        if "theme" in data: session.theme = data["theme"]
        if "date" in data: session.date = data["date"]
        db.session.commit()
        return session.to_dict(), 200

    def delete(self, id):
        session = Session.query.get_or_404(id)
        db.session.delete(session)
        db.session.commit()
        return {"message": "Session deleted"}, 204
