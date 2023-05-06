from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.course_service import create_course, get_courses, get_course_by_id, delete_course, update_course_by_id
from flasgger import swag_from

courses = Blueprint("courses", __name__, url_prefix="/api/v1/courses")


@courses.get('/')
@swag_from('../docs/courses/get_all.yaml')
@jwt_required()
def get_all():
    return get_courses(request.args)


@courses.get('/<int:id>')
@swag_from('../docs/courses/get.yaml')
@jwt_required()
def get_course(id):
    return get_course_by_id(id)


@courses.post('/')
@swag_from('../docs/courses/create.yaml')
@jwt_required()
def create():
    return create_course(request.get_json())


@courses.delete('/<int:id>')
@swag_from('../docs/courses/delete.yaml')
@jwt_required()
def delete(id):
    return delete_course(id)


@courses.put('/<int:id>')
@courses.patch('/<int:id>')
@swag_from('../docs/courses/update.yaml')
@jwt_required()
def update_course(id):
    return update_course_by_id(request.get_json(), id)
