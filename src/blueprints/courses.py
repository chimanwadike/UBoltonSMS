from flask import Blueprint, request
from src.services.course_service import create_course, get_courses, get_course_by_id, delete_course, update_course_by_id
from flasgger import swag_from

courses = Blueprint("courses", __name__, url_prefix="/api/v1/courses")


@courses.get('/')
# @swag_from('../docs/semesters/get_all.yaml')
def get_all():
    return get_courses(request.args)


@courses.get('/<int:id>')
# @swag_from('../docs/semesters/get.yaml')
def get_course(id):
    return get_course_by_id(id)


@courses.post('/')
# @swag_from('../docs/semesters/create.yaml')
def create():
    return create_course(request.get_json())


@courses.delete('/<int:id>')
# @swag_from('../docs/semesters/delete.yaml')
def delete(id):
    return delete_course(id)


@courses.put('/<int:id>')
@courses.patch('/<int:id>')
# @swag_from('../docs/semesters/update.yaml')
def update_course(id):
    return update_course_by_id(request.get_json(), id)
