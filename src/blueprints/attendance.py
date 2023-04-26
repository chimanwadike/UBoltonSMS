from flask import Blueprint, request
from src.services.attendance_service import register_attendance
from flask_jwt_extended import jwt_required
from flasgger import swag_from

attendance = Blueprint("attendance", __name__, url_prefix="/api/v1/attendance")

@attendance.post('/register')
# @swag_from('../docs/courses/get_all.yaml')
@jwt_required()
def register_student_attendance():
    return register_attendance(request.get_json())