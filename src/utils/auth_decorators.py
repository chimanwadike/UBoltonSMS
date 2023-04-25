from functools import wraps

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

from src.constants.http_status_codes import HTTP_403_FORBIDDEN


def admin_required():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_admin"]:
                return func(*args, **kwargs)
            else:
                return jsonify(msg="Admin rights required"), HTTP_403_FORBIDDEN

        return decorator

    return wrapper


def tutor_required():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_tutor"]:
                return func(*args, **kwargs)
            else:
                return jsonify(msg="Tutor rights required"), HTTP_403_FORBIDDEN

        return decorator

    return wrapper


def student_required():
    def wrapper(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["is_student"]:
                return func(*args, **kwargs)
            else:
                return jsonify(msg="Student rights required"), HTTP_403_FORBIDDEN

        return decorator

    return wrapper
