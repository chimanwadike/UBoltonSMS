from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.semester_service import create_semester, get_semesters, get_semester_byid, delete_semester, edit_semester

from flasgger import swag_from

semesters = Blueprint("semesters", __name__, url_prefix="/api/v1/semesters")


@jwt_required()
@semesters.get('/')
@swag_from('../docs/semesters/get_all.yaml')
def get_all():
    return get_semesters(request)


@jwt_required()
@semesters.get('/<int:id>')
@swag_from('../docs/semesters/get.yaml')
def get_semester(id):
    return get_semester_byid(id)


@jwt_required()
@semesters.post('/')
@swag_from('../docs/semesters/create.yaml')
def create():
    return create_semester(request)


@jwt_required()
@semesters.delete('/<int:id>')
@swag_from('../docs/semesters/delete.yaml')
def delete(id):
    return delete_semester(request, id)


@jwt_required()
@semesters.put('/<int:id>')
@semesters.patch('/<int:id>')
@swag_from('../docs/semesters/update.yaml')
def get(id):
    return edit_semester(request, id)



