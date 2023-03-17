from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api/v1/users")


@auth.get('/')
def get():
    return "hello"


@auth.post('login')
def create():
    return "hello"
