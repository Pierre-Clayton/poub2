from app.organizations.models import Organization, OrgUser
from app.organizations.schema import OrganizationSchema, OrganizationPutSchema
from app.utilities.models import db
from app.utilities.resource import BaseResource
from flask import request
from flask_jwt_extended import jwt_required, create_access_token
from sqlalchemy.exc import IntegrityError
import requests
import json

org_schema = OrganizationSchema()
org_schema_list = OrganizationSchema(many=True)
org_put_schema = OrganizationPutSchema()

class OrganizationResource(BaseResource):
    @jwt_required()
    def get(self, id=None):
        """Returns single organization if id is included or All orgs if not set."""

        org_data = {}
        if id is None:
            return {
            "status": 400,
            "success": False,
            "message": "Provide the organization ID"}, 200
        else:
            org = Organization.query.filter_by(id = id).first()
            if not org:
                orgby = Organization.query.filter_by(registered_by = id).first()
                if not orgby:
                    return {
                        "status": 404,
                        "success": False,
                        "data": [],
                        "message": "Organization not found"}, 200
                org = orgby
            org_data = org_schema.dump(org)
            
        return {
            "status": 200,
            "success": True,
            "message": "success",
            "data": org_data}, 200

    @jwt_required()
    def post(self):
        """Requires all fields to be set else returns a 400."""

        org_json = request.get_json()
        try:
            org_data = org_schema.load(org_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "data": [],
                "message": str(e)}, 200
        org_data['org_type'] = 'Individual' if 'org_type' in org_data else org_data['org_type']

        try:
            new_org = Organization.save_to_db(org_data)
            new_org_data = org_schema.dump(new_org)
            org_user_data = {
                "user_id": new_org_data['registered_by'],
                "org_id": new_org_data['id'],
                "user_status": 1,
                "user_type": "ADMIN"
            }
            OrgUser.save_to_db(org_user_data)
            return {
                "status": 201,
                "data": new_org_data,
                "success": True,
                "message": "successfully added organization"}, 200
        except IntegrityError as e:
            db.session.rollback()
            return {
                "status": 400,
                "success": False,
                "data": [],
                "message": f"Missing data: Please ensure all fields are supplied {e}"
            }, 200
        except Exception:
            return {
                "status": 500,
                "success": False,
                "data": [],
                "message": "Internal system error. Please try again"}, 200

    @jwt_required()
    def put(self, id):
        """If id does not match any existing, a new record is created."""

        org = Organization.query.filter_by(id = id).first()
        org_json = request.get_json()
        try:
            org_data = org_put_schema.load(org_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "data": [],
                "message": str(e)}, 200

        if org:
            for field in ["name", "description","location"]:
                setattr(org, field, org_data[field])
            Organization.update_record()
            return {
                "data": org_schema.dump(org),
                "success": True,
                "message": "data updated",
                "status": 201}, 200
        else:
            # treat it as a post request
            try:
                new_org = Organization.save_to_db(org_data)
                return {
                    "data": org_schema.dump(new_org),
                    "status": 201,
                    "success": True,
                    "message": "success"}, 200
            except IntegrityError as e:
                db.session.rollback()
                return {
                    "status": 400,
                    "success": False,
                    "data": [],
                    "message": f"Missing data: Please ensure all fields are supplied  {e}"
                }, 400
            except Exception:
                return {
                    "status": 500,
                    "success": False,
                    "data": [],
                    "message": "Internal system error. Please try again"}, 200









