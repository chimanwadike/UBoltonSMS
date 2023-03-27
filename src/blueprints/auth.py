from flasgger import swag_from
from flask import Blueprint, request

from src.services.auth_service import create_user, authenticate

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
@swag_from('../docs/auth/register.yaml')
def register():
    return create_user(request)


@auth.post('/login')
@swag_from('../docs/auth/login.yaml')
def login():
    return authenticate(request)
