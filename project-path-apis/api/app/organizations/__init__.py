from app.organizations.resource import OrganizationResource, OrgUserResource

from flask import Blueprint
from flask_restful import Api

organization = Blueprint("organization", __name__)
api = Api(organization)

api.add_resource(
    OrganizationResource,
    "/organization",
    "/organization/<id>",
    endpoint="/organization",
)

api.add_resource(
    OrgUserResource,
    "/organization/users",
    "/organization/users/<id>",
    endpoint="/organization/users",
)