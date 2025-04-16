from app.projects.resource import ProjectsResource
from flask import Blueprint
from flask_restful import Api


projects = Blueprint("projects", __name__)

api = Api(projects)
api.add_resource(
    ProjectsResource,
    "/projects",
    "/projects/<id>",
    endpoint="/projects",
)

