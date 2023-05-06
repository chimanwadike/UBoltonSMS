from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.timetable_service import get_course_schedules, get_lesson_sessions_by_tutor
from flasgger import swag_from

schedules = Blueprint("schedules", __name__, url_prefix="/api/v1/timetable")


@schedules.get('/')
@swag_from('../docs/schedules/get_all.yaml')
@jwt_required()
def get_schedules():
    return get_course_schedules(request.args)


@schedules.get('/tutor/<int:tutor_id>/lesson_sessions')
@jwt_required()
def get_lessons_by_tutor(tutor_id):
    return get_lesson_sessions_by_tutor(request.args, tutor_id)
