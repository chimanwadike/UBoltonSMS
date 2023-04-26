import random
import string
from datetime import datetime

from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, LectureSession, TutorCourseAssignment
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity


def generate_check_in_code(lecture_session_id):
    verify_jwt_in_request()
    tutor_id = get_jwt_identity()
    # Get the lecture session with the given ID
    lecture_session = LectureSession.query.get_or_404(lecture_session_id)

    # Get the tutor course assignment for the course
    tutor_course_assignment = TutorCourseAssignment.query.filter_by(
        course_id=lecture_session.lecture_schedule.course_id, user_id=tutor_id
    ).first()

    # Only allow the tutor assigned to the course to generate the check-in code
    if not tutor_course_assignment:
        return jsonify({'error_message': 'Unauthorized'}), HTTP_401_UNAUTHORIZED

    # Check if the lecture session has already ended
    if lecture_session.end_time < datetime.now():
        return jsonify({'error_message': 'Lecture session has ended'}), HTTP_400_BAD_REQUEST

    # Generate the check-in code
    # Generate a random check-in code in the format "AA-BB-CC"
    check_in_code = '-'.join(''.join(random.choices(string.ascii_uppercase, k=2)) for _ in range(3))
    lecture_session.check_in_code = check_in_code
    db.session.commit()

    # Return the updated lecture session as JSON
    return jsonify(lecture_session.to_dict()), HTTP_200_OK


def get_check_in_code(lecture_session_id):
    verify_jwt_in_request()
    tutor_id = get_jwt_identity()
    # Get the lecture session with the given ID
    lecture_session = LectureSession.query.get_or_404(lecture_session_id)

    # Get the tutor course assignment for the course
    tutor_course_assignment = TutorCourseAssignment.query.filter_by(
        course_id=lecture_session.lecture_schedule.course_id, user_id=tutor_id
    ).first()



    # Only allow the tutor assigned to the course to generate the check-in code
    if not tutor_course_assignment:
        return jsonify({'error_message': 'Unauthorized'}), HTTP_401_UNAUTHORIZED

    if not lecture_session.check_in_code:
        return jsonify({'message': 'Check-in code has not been generated for this lecture session.'}), 400
    return jsonify({'check_in_code': lecture_session.check_in_code})


