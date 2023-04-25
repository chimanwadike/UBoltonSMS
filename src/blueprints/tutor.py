from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.timetable_service import get_course_schedules, get_logged_in_tutor_lesson_sessions, \
    get_tutor_lesson_sessions_by_tutor_id
from flasgger import swag_from

from src.utils.auth_decorators import tutor_required, student_required

tutor = Blueprint("tutor", __name__, url_prefix="/api/v1/tutor")


@tutor.get('/my_lesson_sessions')
@tutor_required()
def tutor_get_my_lessons():
    return get_logged_in_tutor_lesson_sessions(request.args)


@tutor.get('/my_lesson_sessions/<int:session_id>')
@tutor_required()
def tutor_get_my_lesson(session_id):
    return get_logged_in_tutor_lesson_sessions(request.args, session_id=session_id)
