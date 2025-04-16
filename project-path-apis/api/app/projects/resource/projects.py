from app.projects.schema import ProjectsSchema
from app.projects.models import Projects
from app.utilities.models import db
from app.utilities.resource import BaseResource
from app.utilities.utils import UtilFunctions
from flask import request, current_app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


utils = UtilFunctions()

projects_schema_list = ProjectsSchema(many=True)
projects_schema = ProjectsSchema()


class ProjectsResource(BaseResource):
    @jwt_required()
    def get(self, id=None):
        """Returns single project if id is included or All projects if org id is set."""
        org_data = {}
        if id is None:
            return {
            "status": 400,
            "success": False,
            "message": "Provide the organization ID"}, 200

        proj = Projects.query.filter_by(id = id).first()
        if not proj:
            projs = Projects.query.filter_by(org_id = id).all()
            if not projs:
                return {
                "status": 404,
                "success": False,
                "data": [],
                "message": "projects not found"}, 200
            org_data = projects_schema_list.dump(projs)
        else:
            org_data = projects_schema.dump(projs)
            
        return {
            "status": 200,
            "success": True,
            "message": "success",
            "data": org_data}, 200

    @jwt_required()
    def post(self):
        """Requires all fields to be set else returns a 400."""

        project_json = request.get_json()
        try:
            project_data = projects_schema.load(project_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "message": str(e)}, 200
        
        try:
            nwsale1 = Projects.save_to_db(project_data)
            
        except:
            db.session.rollback()
        
        return {"status": 200,
                "success": True,
                "data": projects_schema.dump(nwsale1),
                "message": "Success"}, 200
        

    @jwt_required()
    def put(self, id=None):
        """If id does not match any existing, a new record is created."""
        if id is None:
            return {
            "status": 400,
            "success": False,
            "message": "Provide the project ID"}, 200

        org = Projects.query.filter_by(id = id).first()
        org_json = request.get_json()
        try:
            org_data = projects_schema.load(org_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "data": [],
                "message": str(e)}, 200

        if org:
            for field in ["project_name", "project_description","project_start_date","project_status"]:
                setattr(org, field, org_data[field])
            Projects.update_record()
            return {
                "data": projects_schema.dump(org),
                "success": True,
                "message": "data updated",
                "status": 201}, 200
        else:
            
             return {
                    "status": 500,
                    "success": False,
                    "data": [],
                    "message": "Internal system error. Please try again"}, 200


