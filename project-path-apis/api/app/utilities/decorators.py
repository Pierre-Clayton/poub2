from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.utilities.utils import UtilFunctions
utils = UtilFunctions()

def page_not_found_404(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return {
            "status": 404,
            "data": [],
            "success": False,
            "message": "Page not found",
        }, 404

    return wrapper


def sys_admin_login(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        current_user_id = get_jwt_identity()
        from app.user.models import User
        if not User.is_sys_admin(current_user_id):
            return {'status': 401, 'data': [], 'success': False,
                    'message': 'You do not have rights to make this request'
                    }, 401
        return f(*args, **kwargs)
    return wrap
