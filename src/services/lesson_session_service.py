from datetime import datetime

from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from sqlalchemy import desc

from src.constants.http_status_codes import *
from src.database.database_context import db, LectureScheduleUserEnrolment, LectureSchedule, LectureSession, User
from src.utils.utility_functions import get_current_semester


def get_lesson_sessions_for_loggedin_tutor(args, session_id=None):
    verify_jwt_in_request()
    tutor_id = get_jwt_identity()

    assigned_course_schedule_ids = db.session.query(LectureScheduleUserEnrolment.lecture_schedule_id) \
        .join(LectureScheduleUserEnrolment.lecture_schedule) \
        .filter(LectureScheduleUserEnrolment.user_id == tutor_id, LectureScheduleUserEnrolment.user_type == 'tutor',
                LectureSchedule.semester_id == get_current_semester())

    lecture_sessions = LectureSession \
        .query.order_by(desc(LectureSession.end_time)) \
        .filter(LectureSession.lecture_schedule_id.in_(assigned_course_schedule_ids),
                LectureSession.end_time <= datetime.now())

    data = ""

    if session_id is None:
        data = [session.to_dict() for session in lecture_sessions]
    else:
        single_data = lecture_sessions.filter(LectureSession.id == session_id).first()
        if single_data is not None:
            data = single_data.to_dict()
        else:
            return jsonify({'error': 'Lesson session not found'}), HTTP_404_NOT_FOUND

    return jsonify({'data': data}), HTTP_200_OK


def get_students_enrolled_in_lesson_session(args, session_id):
    lecture_session = LectureSession.query \
        .filter(LectureSession.id == session_id) \
        .first()

    if lecture_session is None:
        return jsonify({'error': 'Lecture session not found'}), HTTP_404_NOT_FOUND

    scheduled_students = db.session.query(User)\
        .join(LectureScheduleUserEnrolment)\
        .join(LectureSchedule)\
        .filter(LectureScheduleUserEnrolment.lecture_schedule_id == lecture_session.lecture_schedule_id,
                LectureScheduleUserEnrolment.user_type == 'student',
                LectureSchedule.semester_id == get_current_semester())

    data = [student.to_dict() for student in scheduled_students]

    return jsonify({'data': data}), HTTP_200_OK
