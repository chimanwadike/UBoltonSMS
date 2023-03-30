from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, Course


def create_course(data):
    code = data.get('code')
    title = data.get('title')
    description = data.get('description')

    # Query the database for a course with the given code
    existing_course = Course.query.filter_by(code=code).first()

    if existing_course:
        return jsonify({'error_message': 'A course with with the same code already exists'}), \
            HTTP_409_CONFLICT

    new_course = Course(
        code=code,
        title=title,
        description=description
    )
    db.session.add(new_course)
    db.session.commit()

    return jsonify(new_course.to_dict()), HTTP_201_CREATED


def get_courses(args):
    page = args.get('page', 1, type=int)

    per_page = args.get('per_page', 5, type=int)

    courses = Course.query.paginate(page=page, per_page=per_page)

    # List Comprehension. I have in included the to_dict function in the Course Class
    data = [course.to_dict() for course in courses]

    meta = {
        'page': courses.page,
        'pages': courses.pages,
        'total_count': courses.total,
        'prev_page': courses.prev_num,
        'next_page': courses.next_num,
        'has_next': courses.has_next,
        'has_prev': courses.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


def get_course_by_id(id):
    course = Course.query.get(id)
    if course:
        return jsonify(course.to_dict()), HTTP_200_OK
    else:
        return jsonify({'error_message': 'Course not found'}), HTTP_404_NOT_FOUND


def update_course_by_id(data, id):
    course = Course.query.get(id)

    if not course:
        return jsonify({'error_message': 'Course not found'}), HTTP_404_NOT_FOUND

    # Get the updated values from the request body
    code = data.get('code')
    title = data.get('title')
    description = data.get('description')

    # Check if the variables are not empty then Update the course attributes with the new values
    if code:
        course.code = code
    if title:
        course.title = title
    if description:
        course.description = description

    db.session.commit()
    return jsonify(course.to_dict()), HTTP_200_OK


def delete_course(id):
    course = Course.query.get(id)
    if course:
        db.session.delete(course)
        db.session.commit()
        return jsonify({}), HTTP_204_NO_CONTENT
    else:
        return jsonify({'error': 'Course not found'}), HTTP_404_NOT_FOUND


