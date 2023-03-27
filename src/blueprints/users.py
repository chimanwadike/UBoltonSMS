from flasgger import swag_from
from flask import Blueprint, request
from src.services.auth_service import create_user
from src.services.user_service import get_users, get_user, edit_user, delete_user

user = Blueprint("user", __name__, url_prefix="/api/v1/users")


@user.post('/')
@swag_from('../docs/users/create.yaml')
def create():
    return create_user(request)


@user.get('/')
@swag_from('../docs/users/get_all.yaml')
def get_all():
    return get_users(request)


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
