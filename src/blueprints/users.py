from flasgger import swag_from
from flask import Blueprint, request
from src.services.user_service import create_user, get_users, get_user, edit_user, delete_user

# auth = Blueprint("auth", __name__, url_prefix="/api/v1/users")

user = Blueprint("user", __name__, url_prefix="/api/v1/users")




# @auth.get('/')
# def get():
#     return "hello"


# @auth.post('login')
# def create():
#     return "hello"

# register a user
@user.post('/')
@swag_from('../docs/users/create.yaml')
def create():
    return create_user(request)

# get all users
@user.get('/')
@swag_from('../docs/users/get_all.yaml')
def get_all():
    return get_users(request)

# get a single user using the user id
@user.get('/<int:id>')
@swag_from('../docs/users/get.yaml')
def get_one_user(id):
    return get_user(request, id)

@user.patch('/<int:id>')
@user.put('/<int:id>')
@swag_from('../docs/users/update.yaml')
def update_user(id):
    return edit_user(request, id)

@user.delete('/<int:id>')
@swag_from('../docs/users/delete.yaml')
def delete_one_user(id):
    return delete_user(request, id)