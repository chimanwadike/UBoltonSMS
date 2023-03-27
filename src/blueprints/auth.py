from flasgger import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.auth_service import create_user, authenticate, token_refresh

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('/register')
@swag_from('../docs/auth/register.yaml')
def register():
    return create_user(request)


@auth.post('/login')
@swag_from('../docs/auth/login.yaml')
def login():
    return authenticate(request)


@jwt_required(refresh=True)
@auth.post('/token/refresh')
@swag_from('../docs/auth/token_refresh.yaml')
def refresh_user_token():
    return token_refresh(request)
