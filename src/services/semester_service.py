import json
from datetime import datetime

from flask import jsonify

from src.constants.http_status_codes import HTTP_200_OK
from src.database.database_context import db, Semester, User


def get_semesters():
    semesters = Semester.query.all()
    data = []
    for semester in semesters:
        data.append({'id': semester.id, 'name': semester.name})

    return jsonify({'data': data}), HTTP_200_OK


def create_semester(self):
    data = self
    start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
    name = data['name']

    #    semester_exist = Semester.query.filter_by(id=1).first()

    semester = Semester(start_date=start_date, end_date=end_date, name=name)
    db.session.add(semester)
    db.session.commit()

    return jsonify(
        {'id': semester.id,
         'name': semester.name,
         'start_date': semester.start_date,
         'end_date': semester.end_date
         }
    ), HTTP_200_OK
