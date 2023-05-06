from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.semester_service import create_semester, get_semesters, get_semester_byid, delete_semester, edit_semester

from flasgger import swag_from

semesters = Blueprint("semesters", __name__, url_prefix="/api/v1/semesters")


@semesters.get('/')
@swag_from('../docs/semesters/get_all.yaml')
@jwt_required()
def get_all():
    return get_semesters(request)


@semesters.get('/<int:id>')
@swag_from('../docs/semesters/get.yaml')
@jwt_required()
def get_semester(id):
    return get_semester_byid(id)


@semesters.post('/')
@swag_from('../docs/semesters/create.yaml')
@jwt_required()
def create():
    return create_semester(request)


@semesters.delete('/<int:id>')
@swag_from('../docs/semesters/delete.yaml')
@jwt_required()
def delete(id):
    return delete_semester(request, id)


@semesters.put('/<int:id>')
@semesters.patch('/<int:id>')
@swag_from('../docs/semesters/update.yaml')
@jwt_required()
def get(id):
    return edit_semester(request, id)