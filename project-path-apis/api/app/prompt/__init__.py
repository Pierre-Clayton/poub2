from app.prompt.resource import RetrievalResource
from flask import Blueprint
from flask_restful import Api


prompt = Blueprint("prompt", __name__)

api = Api(prompt)
api.add_resource(
    RetrievalResource,
    "/prompt",
    "/prompt/<id>",
    endpoint="/prompt",
)

