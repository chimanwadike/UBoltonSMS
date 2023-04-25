from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.timetable_service import get_course_schedules, get_logged_in_tutor_lesson_sessions, \
    get_tutor_lesson_sessions_by_tutor_id
from flasgger import swag_from

from src.utils.auth_decorators import tutor_required, student_required

schedules = Blueprint("schedules", __name__, url_prefix="/api/v1/timetable")


@schedules.get('/')
@swag_from('../docs/schedules/get_all.yaml')
def get_schedules():
    return get_course_schedules(request.args)


@schedules.get('/tutor/my_lesson_sessions')
@tutor_required()
def tutor_get_my_lessons():
    return get_logged_in_tutor_lesson_sessions(request.args)


@schedules.get('/tutor/<int:id>/lesson_sessions')
def get_lessons_tutor_id(id):
    return get_tutor_lesson_sessions_by_tutor_id(request.args, id)
