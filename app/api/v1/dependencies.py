from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.user import User
from app.core.exceptions import ForbiddenException


def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)

            if not user or user.role != required_role:
                raise ForbiddenException("You do not have permission")

            return fn(*args, **kwargs)
        return wrapper
    return decorator