from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post('register')
def register():
    return "user created"


@auth.post('login')
def login():
    return "user logged in"
