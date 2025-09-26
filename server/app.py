from flask import Flask
from flask_restful import Api
from extensions import db, migrate, cors, jwt
from resources import (
    MeResource,
    UserListResource, UserResource,
    SessionListResource, SessionResource, JoinSessionResource,
    ReflectionListResource, ReflectionResource
)
from auth import Register, Login


app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = '7c417c716e1c3133a094a5661460efc2'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bibleclub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


migrate.init_app(app, db)

cors.init_app(app)
jwt.init_app(app)
db.init_app(app)
api = Api(app)


api.add_resource(MeResource, "/me")

api.add_resource(UserListResource, "/users")
api.add_resource(UserResource, "/users/<int:id>")

api.add_resource(SessionListResource, "/sessions")
api.add_resource(SessionResource, "/sessions/<int:id>")
api.add_resource(JoinSessionResource, "/sessions/<int:session_id>/join")


api.add_resource(ReflectionListResource, "/reflections")
api.add_resource(ReflectionResource, "/reflections/<int:id>")

api.add_resource(Register, "/register")
api.add_resource(Login, "/login")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)
