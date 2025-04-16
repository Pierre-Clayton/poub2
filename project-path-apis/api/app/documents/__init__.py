from app.documents.resource import ProjectDocumentsResource, UploadDocumentsResource
from flask import Blueprint
from flask_restful import Api


documents = Blueprint("documents", __name__)

api = Api(documents)
api.add_resource(
    ProjectDocumentsResource,
    "/documents",
    "/documents/<id>",
    endpoint="/documents",
)

api.add_resource(
    UploadDocumentsResource,
    "/documents/upload",
    endpoint="/documents/upload",
)