from app.organizations.models import OrgUser
from app.organizations.schema import OrgUserSchema
from app.organizations.models import Organization
from app.utilities.models import db
from app.utilities.resource import BaseResource
from flask import request
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError

org_user_schema = OrgUserSchema()
org_user_schema_list = OrgUserSchema(many=True)


class OrgUserResource(BaseResource):
    @jwt_required()
    def get(self, id=None):
        """Returns single or list record.

        - single org_user if id is that of org_user
        - list of org_user records with user or org if id is of [user, org]
        - All org_users if id is not set.
        """

        org_user_data = {}
        if id is None:
            org = OrgUser.find_all()
            org_user_data = org_user_schema_list.dump(org)
        else:
            org_user_data = OrgUser.find_by_id(id)
            if org_user_data:
                return {
                    "status": 200,
                    "success": True,
                    "message": "success",
                    "data": org_user_data}, 200
                    
            if not org_user_data:
                # return all records with user (orgs user is in)
                org_user_data = OrgUser.query.filter_by(user_id=id)
                org_user_data = org_user_schema_list.dump(org_user_data)
                data_org_user = []
                for org in org_user_data:
                    ordata = Organization.find_by_id(org['org_id'])
                    data_org_user.append({
                        "org_id": str(org['org_id']),
                        "user_type":org['user_type'],
                        "user_status": org['user_status'],
                        "user_orgname": ordata.name,
                        "org_type": ordata.org_type if ordata.org_type is not None else "Individual"})
                org_user_data = data_org_user

            if not org_user_data:
                # return all records with org_id (users in the org)
                org_user_data = OrgUser.query.filter_by(org_id=id)
                org_user_data = org_user_schema_list.dump(org_user_data)
            if not org_user_data:
                # return specific org_user record
                org_user_data = OrgUser.find_by_id(id)
                org_user_data = org_user_schema.dump(org_user_data)
            if not org_user_data:
                return {
                    "status": 404,
                    "success": False,
                    "data": [],
                    "message": "OrgUser not found"}, 200
        return {
            "status": 200,
            "success": True,
            "message": "success",
            "data": org_user_data}, 200


    @jwt_required()
    def put(self, id):
        """If id does not match any existing, a new record is created."""

        org_user = OrgUser.query.filter_by(user_id=id).first()
        org_user_json = request.get_json()
        try:
            org_user_data = org_user_schema.load(org_user_json)
        except Exception as e:
            return {"status": 400,
                "data":[], "success": False,
                "message": str(e)}, 200

        if org_user:
            for field in ["user_status","user_type"]:
                setattr(org_user, field, str(org_user_data[field]))
            OrgUser.update_record()
            return {"status": 201,"data": org_user_schema.dump(org_user),"success": True, "message": "added successfully"}, 201
        else:
            try:
                org_user_data['user_type'] = 'VIEWER'
                new_org_user = OrgUser.save_to_db(org_user_data)
                return {"status": 201,"data":org_user_schema.dump(new_org_user),"success": True, "message": "added successfully"}, 201
            except IntegrityError as e:
                db.session.rollback()
                return {
                    "status": 400,
                    "message": "Missing data: Please ensure all fields are supplied",
                    "success": False
                }, 200
            except Exception:
                return {
                    "status": 500,
                    "message": "Internal system error. Please try again",
                    "success": False}, 200
