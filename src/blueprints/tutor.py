from flask import Blueprint, request

from src.services.lesson_session_service import get_lesson_sessions_for_loggedin_tutor

from src.utils.auth_decorators import tutor_required

tutor = Blueprint("tutor", __name__, url_prefix="/api/v1/tutor")


@tutor.get('/my_lesson_sessions')
@tutor_required()
def tutor_get_my_lessons():
    return get_lesson_sessions_for_loggedin_tutor(request.args)


@tutor.get('/my_lesson_sessions/<int:session_id>')
@tutor_required()
def tutor_get_my_lesson(session_id):
    return get_lesson_sessions_for_loggedin_tutor(request.args, session_id=session_id)
