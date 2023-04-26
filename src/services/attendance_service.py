from datetime import datetime
from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, LectureSession, LectureSessionAttendance, \
    StudentCourseEnrolment
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def register_attendance(data):
    verify_jwt_in_request()
    student_id = get_jwt_identity()
    check_in_code = data.get('check_in_code')

    # Check if check-in code is valid
    lecture_session = LectureSession.query.filter_by(check_in_code=check_in_code).first()
    if not lecture_session:
        return jsonify({'message': 'Invalid check-in code'}), HTTP_400_BAD_REQUEST
    if not lecture_session.allow_self_registration:
        return jsonify({'message': 'Self-registration not allowed for this session'}), HTTP_400_BAD_REQUEST
    if lecture_session.end_time < datetime.now():
        return jsonify({'message': 'Lecture session has ended'}), HTTP_400_BAD_REQUEST

    # # Check if user_id is valid
    # user = User.query.filter_by(id=student_id).first()
    # if not user:
    #     return jsonify({'message': 'Invalid user ID'}), HTTP_400_BAD_REQUEST

    # Check if student is enrolled in the course for which the lecture session is being held
    if not StudentCourseEnrolment.query.filter_by(user_id=student_id,
                                                  course_id=lecture_session.lecture_schedule.course_id).first():
        return jsonify({'message': 'Not enrolled in this course'}), HTTP_400_BAD_REQUEST

    # Check if student has already registered for this lecture session
    if LectureSessionAttendance.query.filter_by(lecture_session_id=lecture_session.id, user_id=student_id).first():
        return jsonify({'message': 'Attendance already registered'}), HTTP_400_BAD_REQUEST

    attendance = LectureSessionAttendance(
        lecture_session_id=lecture_session.id,
        user_id=student_id,
        attendance_status_code='P'
    )

    db.session.add(attendance)
    db.session.commit()

    return jsonify(attendance.to_dict()), HTTP_200_OK
