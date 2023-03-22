from flask import Blueprint, request
from src.services.semester_service import create_semester, get_semesters, get_semester, delete_semester, edit_semester
from flasgger import swag_from

semesters = Blueprint("semesters", __name__, url_prefix="/api/v1/semesters")


@semesters.get('/')
@swag_from('../docs/semesters/get_all.yaml')
def get_all():
    return get_semesters(request)


@semesters.get('/<int:id>')
@swag_from('../docs/semesters/get.yaml')
def get_semester(id):
    return get_semester(request, id)


@semesters.post('/')
@swag_from('../docs/semesters/create.yaml')
def create():
    return create_semester(request)


@semesters.delete('/<int:id>')
def delete(id):
    return delete_semester(request, id)


@semesters.put('/<int:id>')
@semesters.patch('/<int:id>')
@swag_from('../docs/semesters/update.yaml')
def get(id):
    return edit_semester(request, id)
