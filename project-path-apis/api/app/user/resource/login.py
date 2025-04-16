from app.user.models import User
from app.user.schema import LoginWebInputSchema
from app.utilities.resource import BaseResource
from app.utilities.utils import UtilFunctions
from flask import request, current_app
from flask_jwt_extended import create_access_token, create_refresh_token
import bcrypt
from datetime import datetime

login_web_input_schema = LoginWebInputSchema()
utils = UtilFunctions()



class LoginWebResource(BaseResource):
    def post(self):
        """Checks if auth credentials are correct then returns a token."""

        log_json = request.get_json()
        
        try:
            data = login_web_input_schema.load(log_json)
        except Exception as e:
            return {
                "status": 400,
                "success": False,
                "message": str(e),
                "data": ["nothis"]
                }, 200
    
        if 'google_id_token' in data:
            # Google Login
            id_info = utils.verify_google_token(data['google_id_token'])
            if not id_info:
                return {'message': 'Invalid Google token'}, 400

            user = User.query.filter_by(
                email=id_info['email'],
                google_id=id_info['sub'], status=1
            ).first()
        else:
            # Regular Login
            
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return {'message': 'Missing email or password', 'status': 400,'success': False}, 200

            user = User.query.filter_by(
                email=email,
                status = 1
            ).first()

            if not user:
                return {'message': 'User not found or is inactive','status': 404, 'success': False}, 200

            if not User.is_valid(email,password):
                return {'message': 'Invalid credentials', 'status': 401, 'success':False}, 200

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {'message': 'success','token': access_token,'refresh_token':refresh_token, 'success': True, "user_id": str(user.id)}, 200