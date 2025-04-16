from app.documents.schema import ProjectDocumentsSchema
from app.documents.models import ProjectDocuments
from app.utilities.models import db
from app.utilities.resource import BaseResource
from flask import request, current_app
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

# from google.cloud import storage


documents_schema = ProjectDocumentsSchema()
documents_schema_list = ProjectDocumentsSchema(many=True)


class ProjectDocumentsResource(BaseResource):

    @jwt_required()
    def get(self, id=None):
        """Returns single organization if id is included or All orgs if not set."""
        ident = get_jwt_identity()
        org_data = {}
        if id is None:
            return {
                "status": 404,
                "message": "You have to add organization id",
                "success": False,
                "data":[]
            }

        org = ProjectDocuments.query.filter_by(project_id=id,added_by = str(ident)).all()
        if not org:
            org = ProjectDocuments.query.filter_by(org_id=id,added_by = str(ident)).all()
        org_data = documents_schema_list.dump(org)
           
        return {
            "status": 200,
            "message": "success",
            "success": True,
            "data": org_data}, 200

    