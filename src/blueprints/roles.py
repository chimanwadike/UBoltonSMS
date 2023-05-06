from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.role_service import create_role, get_roles, get_role, delete_role, edit_role
from flasgger import swag_from

roles = Blueprint("roles", __name__, url_prefix="/api/v1/roles")


@roles.get('/')
@swag_from('../docs/roles/get_all.yaml')
@jwt_required()
def get_all():
    return get_roles(request)


@roles.get('/<int:id>')
@swag_from('../docs/roles/get.yaml')
@jwt_required()
def get_role(id):
    return get_role(request, id)


@roles.post('/')
@swag_from('../docs/roles/create.yaml')
@jwt_required()
def create():
    return create_role(request)


@roles.delete('/<int:id>')
@swag_from('../docs/roles/delete.yaml')
@jwt_required()
def delete(id):
    return delete_role(request, id)


@roles.put('/<int:id>')
@roles.patch('/<int:id>')
@swag_from('../docs/roles/update.yaml')
@jwt_required()
def get(id):
    return edit_role(request, id)
