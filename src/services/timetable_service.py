from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, Course, LectureSchedule, LectureSession
from src.utils.utility_functions import get_current_semester


def get_course_schedules(args):
    page = args.get('page', 1, type=int)

    per_page = args.get('per_page', 5, type=int)

    course_schedules = LectureSchedule.query \
        .filter(LectureSchedule.semester_id == get_current_semester()) \
        .paginate(page=page, per_page=per_page)

    data = [schedule.to_dict() for schedule in course_schedules]

    meta = {
        'page': course_schedules.page,
        'pages': course_schedules.pages,
        'total_count': course_schedules.total,
        'prev_page': course_schedules.prev_num,
        'next_page': course_schedules.next_num,
        'has_next': course_schedules.has_next,
        'has_prev': course_schedules.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


def get_student_course_sessions(args):
    student_id = 1  # TODO:: change hardcoded value
    return None


def get_tutor_course_sessions(args):
    student_id = 1  # TODO:: change hardcoded value
    return None


def get_enrolled_course_students(args):
    tutor_id = 1  # TODO:: change hardcoded value
    return None


def get_tutor_assigned_courses(args):
    student_id = 1  # TODO:: change hardcoded value
    return None


def get_tutor_assigned_course_schedule(args):
    student_id = 1  # TODO:: change hardcoded value
    return None
