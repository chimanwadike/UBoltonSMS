from flask import Blueprint, request
from src.services.attendance_service import register_attendance, get_student_attendance_history
from flask_jwt_extended import jwt_required
from src.utils.auth_decorators import student_required

attendance = Blueprint("attendance", __name__, url_prefix="/api/v1/attendance")


@attendance.post('/register')
@student_required()
def register_student_attendance():
    return register_attendance(data=request.get_json())


@attendance.get('/all')
@student_required()
def get_all_attendance():
    return get_student_attendance_history()
