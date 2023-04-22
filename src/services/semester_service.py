import json
from datetime import datetime

from flask import jsonify
from sqlalchemy import extract

from src.constants.http_status_codes import *
from src.database.database_context import db, Semester


def get_semesters(self):
    page = self.args.get('page', 1, type=int)

    per_page = self.args.get('per_page', 5, type=int)

    semesters = Semester.query.paginate(page=page, per_page=per_page)

    data = []
    for semester in semesters.items:
        data.append({'id': semester.id, 'name': semester.name})

    meta = {
        'page': semesters.page,
        'pages': semesters.pages,
        'total_count': semesters.total,
        'prev_page': semesters.prev_num,
        'next_page': semesters.next_num,
        'has_next': semesters.has_next,
        'has_prev': semesters.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


def get_semester(self, id):
    data = self.get_json()
    semester = Semester.query \
        .filter(Semester.id == id) \
        .first()

    if not semester:
        return jsonify({'error_message': 'Semester does not exist'}), HTTP_404_NOT_FOUND

    return jsonify(
        {'id': semester.id,
         'name': semester.name,
         'start_date': semester.start_date,
         'end_date': semester.end_date
         }
    ), HTTP_200_OK


def create_semester(self):
    data = self.get_json()
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    name = data['name']

    semester_exist = Semester.query \
        .filter(extract('year', Semester.start_date) == start_date.year) \
        .filter(extract('month', Semester.start_date) == start_date.month) \
        .first()

    if semester_exist:
        return jsonify({'error_message': 'A semester with the same start year and month already exists'}), \
            HTTP_409_CONFLICT

    semester = Semester(start_date=start_date, end_date=end_date, name=name)
    db.session.add(semester)
    db.session.commit()

    return jsonify(
        {'id': semester.id,
         'name': semester.name,
         'start_date': semester.start_date,
         'end_date': semester.end_date
         }
    ), HTTP_201_CREATED


def delete_semester(self, id):
    semester = Semester.query \
        .filter(Semester.id == id) \
        .first()

    if not semester:
        return jsonify({'message': 'Semester does not exist'}), HTTP_404_NOT_FOUND

    db.session.delete(semester)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT


def edit_semester(self, id):
    data = self.get_json()

    semester = Semester.query \
        .filter(Semester.id == id) \
        .first()

    if not semester:
        return jsonify({'message': 'Semester does not exist'}), HTTP_404_NOT_FOUND

    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()

    semester.name = data['name']
    semester.start_date = start_date
    semester.end_date = end_date

    db.session.commit()

    return jsonify(
        {'id': semester.id,
         'name': semester.name,
         'start_date': semester.start_date,
         'end_date': semester.end_date
         }
    ), HTTP_200_OK

