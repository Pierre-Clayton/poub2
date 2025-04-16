from app.user.models import RevokedToken
from app.utilities.resource import BaseResource
from flask_jwt_extended import get_jwt, jwt_required


class LogoutResource(BaseResource):
    @jwt_required()
    def delete(self):
        """Adds jti to revoked tokens effectively rendering it unusable"""
        jti = get_jwt()["jti"]
        try:
            RevokedToken.save_to_db({"jti": jti})
            return {
                "status": 200,
                "success": True,
                "message": "success"}, 200
        except Exception:
            return {
                "status": 500,
                "success": False,
                "message": "Internal system error. Please try again"}, 200
