import random
import string
from datetime import datetime

from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, LectureSession, TutorCourseAssignment
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

def register_attendance():
    verify_jwt_in_request()
    student_id = get_jwt_identity()
    data = request.get_json()
    check_in_code = data.get('check_in_code')


    # Check if check-in code is valid
    lecture_session = LectureSession.query.filter_by(check_in_code=check_in_code).first()
    if not lecture_session:
        return jsonify({'message': 'Invalid check-in code'}), 400
    if lecture_session.check_in_code != 'P':
        return jsonify({'message': 'Self-registration not allowed for this session'}), 400
    if lecture_session.end_time < datetime.now():
        return jsonify({'message': 'Lecture session has ended'}), 400

    # Check if user_id is valid
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'Invalid user ID'}), 400

    # Check if user has already registered for this lecture session
    if LectureSessionAttendance.query.filter_by(lecture_session_id=lecture_session.id, user_id=user_id).first():
        return jsonify({'message': 'Attendance already registered'}), 400

    # Create new attendance instance
    attendance = LectureSessionAttendance(
        lecture_session_id=lecture_session.id,
        user_id=user_id,
        attendance_status_code='P'
    )

    # Save to database
    db.session.add(attendance)
    db.session.commit()

    # Return attendance data
    return jsonify(attendance.to_dict()), 200