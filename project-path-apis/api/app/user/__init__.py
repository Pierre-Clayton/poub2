from app.user.resource import LoginWebResource, RegisterResource, LogoutResource
from flask import Blueprint
from flask_restful import Api

user = Blueprint("user", __name__)
api = Api(user)


api.add_resource(LoginWebResource, "/user/login", endpoint="/user/login")

api.add_resource(RegisterResource, "/user/signup", "/user/signup/<id>",endpoint="/user/signup")

api.add_resource(LogoutResource, "/user/logout", endpoint="/user/logout")


