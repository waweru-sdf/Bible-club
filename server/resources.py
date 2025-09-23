from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Session, UserSession, Reflection
from datetime import datetime

# ----------user----------
class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [u.to_dict() for u in users], 200


class UserResource(Resource):
    def get(self, id):
        user = User.query.get_or_404(id)
        return user.to_dict(), 200

    def patch(self, id):
        user = User.query.get_or_404(id)
        data = request.get_json()
        if "name" in data: user.name = data["name"]
        if "email" in data: user.email = data["email"]
        if "password" in data: user.set_password(data["password"])
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

    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()  # logged in user ID

        session = Session(
            title=data["title"],
            theme=data["theme"],
            date=data["date"],
            facilitator_id=current_user
        )
        db.session.add(session)
        db.session.commit()

        user_session = UserSession(user_id=current_user, session_id=session.id, role="facilitator")
        db.session.add(user_session)
        db.session.commit()

        return session.to_dict(), 201


class SessionResource(Resource):
    def get(self, id):
        session = Session.query.get_or_404(id)
        return session.to_dict(), 200

    @jwt_required()
    def patch(self, id):
        session = Session.query.get_or_404(id)
        data = request.get_json()
        if "title" in data: session.title = data["title"]
        if "theme" in data: session.theme = data["theme"]
        if "date" in data: session.date = data["date"]
        db.session.commit()
        return session.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        session = Session.query.get_or_404(id)
        db.session.delete(session)
        db.session.commit()
        return {"message": "Session deleted"}, 204


# ----------session join----------
class SessionJoinResource(Resource):
    @jwt_required()
    def post(self, id):
        current_user = get_jwt_identity()
        user_session = UserSession(user_id=current_user, session_id=id, role="participant")
        db.session.add(user_session)
        db.session.commit()
        return user_session.to_dict(), 201


# ----------reflection----------
class ReflectionListResource(Resource):
    def get(self):
        reflections = Reflection.query.all()
        return [r.to_dict() for r in reflections], 200

    @jwt_required()
    def post(self):
        data = request.get_json()
        current_user = get_jwt_identity()
        reflection = Reflection(
            content=data["content"],
            user_id=current_user,
            session_id=data["session_id"]
        )
        db.session.add(reflection)
        db.session.commit()
        return reflection.to_dict(), 201


class ReflectionResource(Resource):
    def get(self, id):
        reflection = Reflection.query.get_or_404(id)
        return reflection.to_dict(), 200

    @jwt_required()
    def patch(self, id):
        reflection = Reflection.query.get_or_404(id)
        data = request.get_json()
        if "content" in data: reflection.content = data["content"]
        db.session.commit()
        return reflection.to_dict(), 200

    @jwt_required()
    def delete(self, id):
        reflection = Reflection.query.get_or_404(id)
        db.session.delete(reflection)
        db.session.commit()
        return {"message": "Reflection deleted"}, 204
