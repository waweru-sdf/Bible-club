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
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_url_path="/", static_folder="./client/build")
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bibleclub.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#render index route
@app.route("/")
def index():
    return app.send_static_file("index.html")

#render 404 route pate
@app.errorhandler(404)
def not_found(err):
    return app.send_static_file("index.html")



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
    app.run(debug=False, port=5003)
