from app.psychometrics.resource import PsychometricsResource, PsychometricsTypesResource
from flask import Blueprint
from flask_restful import Api


psychometrics = Blueprint("psychometrics", __name__)

api = Api(psychometrics)
api.add_resource(
    PsychometricsResource,
    "/psychometrics",
    "/psychometrics/<id>",
    endpoint="/psychometrics",
)

api.add_resource(
    PsychometricsTypesResource,
    "/psychometrics/types",
    endpoint="/psychometrics/types",
)