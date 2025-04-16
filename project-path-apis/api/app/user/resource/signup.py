from app.user.schema import UserSchema, UserRegSchema,UserPUTSchema
from app.user.models import User, db
from app.utilities.resource import BaseResource
from app.utilities.utils import UtilFunctions, EMAILSENDER
from app.utilities.decorators import sys_admin_login
from flask_jwt_extended import jwt_required

from flask import request, current_app
import requests
import json

utils = UtilFunctions()
email = EMAILSENDER()
reg_schema = UserRegSchema()
user_schema_list = UserSchema(many=True)
edit_user_schema = UserPUTSchema()


class RegisterResource(BaseResource):
    @jwt_required()
    @sys_admin_login
    def get(self, id=None):
        """Returns single contact if id is included or All contacts if not set."""

        querry_data = {}
        if id is None:
            contacts = User.query.all()
            alldts = user_schema_list.dump(contacts)
            return {
                "status": 200,
                "message": "request",
                "data": alldts,
                "success": True
            }, 200
        else:
            contacts = User.query.filter_by(id=id).first()
            if not contacts:
                return {
                    "status": 404,
                    "message": "contact not found",
                    "success": False}, 200
            
            querry_data = user_schema_list.dump(contacts)
        return {
            "status": 200,
            "message": "success",
            "success": True,
            "data": querry_data}, 200

    def post(self):
        """Checks if auth credentials are correct then:

        - Creates a user
        - Creates an auth user
        """

        auth_json = request.get_json()
        current_app.logger.error(auth_json)
        try:
            data = reg_schema.load(auth_json)
        except Exception as e:
            return {
                "status": 400,
                "message": str(e),
                "success": False}, 200

        if 'google_id_token' in data:
            # Google Signup
            id_info = utils.verify_google_token(data['google_id_token'])
            if not id_info:
                return {'message': 'Invalid Google token', 'success': False, 'status':400}, 200

            email = id_info['email']
            google_id = id_info['sub']
            username = id_info.get('name', email.split('@')[0])

            if User.query.filter_by(email=email).first():
                return {'message': 'Email already registered', 'status': 400, 'success': False}, 200

            # Generate unique username if needed
            base_username = username
            counter = 1
            while User.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1

            new_user = {
                "username": username,
                "email": email,
                "google_id": google_id,
                "status": 0
            }
        else:
            # Regular Signup
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not all([username, email, password]):
                return {'message': 'Missing required fields','status': 400,'success': False}, 200

            if User.query.filter((User.username == username) | (User.email == email)).first():
                return {'message': 'Username or email already exists', 'status': 400,'success': False}, 200

            
            new_user = {
                "username": username,
                "email": email,
                "password_hash": User.hash_pwd(password),
                "status": 0
            }
                
        try:
            n_user = User.save_to_db(new_user)
        except Exception as e:
            db.session.rollback()
            return {'message': 'Registration failed', 'error': str(e),}, 400

        return {"success": True, "status":201,"message":"user registered successfully", "user_id": str(n_user.id)}, 201

    @jwt_required()
    @sys_admin_login
    def put(self, id=None):
        if id is None:
            return {
                "status": 500,
                "message": "pass the message or business id with your request",
                "success": False
            }, 200
        group_json = request.get_json()
        try:
            group_data = edit_user_schema.load(group_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "message": str(e)}, 200

        try:
            grp = User.query.filter_by(id = id).first()
            
            for field in ["status"]:
                setattr(grp, field, group_data[field])
            User.update_record()
            if group_data['status'] == 1:
                tdata = {"name": f"{grp.username}"}
                email.SendDynamicSlim([group_data['email']],current_app.config['SENDGRID_APPROVE_EMAIL_TEMP'],tdata)
    
            return {
                "status": 200,
                "success": True,
                "message": 'UPDATED'}, 200
        except Exception as e:
            db.session.rollback()
            return {
                "status": 400,
                "success": False,
                "message": f'error encountered - {e}'}, 200



        