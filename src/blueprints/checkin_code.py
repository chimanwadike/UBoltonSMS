from flask import Blueprint, request
from src.services.checkin_code_service import generate_check_in_code, get_check_in_code
from flask_jwt_extended import jwt_required
from src.utils.auth_decorators import tutor_required


checkin_code = Blueprint("checkin_code", __name__, url_prefix="/api/v1/checkin_code")


@checkin_code.post('/<int:id>/generate_check_in_code')
@tutor_required()
def generate_checkin_code(id):
    return generate_check_in_code(lecture_session_id=id)

@checkin_code.get('/<int:id>/view_check_in_code')
@tutor_required()
def get_checkin_code(id):
    return get_check_in_code(lecture_session_id=id)