from functools import wraps
from http import HTTPStatus
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def role_required(is_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims['sub'][is_role]:
                return fn(*args, **kwargs)
            else:
                return jsonify({'msg': 'Insufficient permission.'}), HTTPStatus.FORBIDDEN

        return decorator

    return wrapper
