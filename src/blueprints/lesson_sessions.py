from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.lesson_session_service import get_students_enrolled_in_lesson_session

lesson_sessions = Blueprint("lesson_sessions", __name__, url_prefix="/api/v1/lesson_sessions")


@lesson_sessions.get('/<int:session_id>/students')
@jwt_required()
def students_by_lesson_session(session_id):
    return get_students_enrolled_in_lesson_session(request.args, session_id=session_id)
