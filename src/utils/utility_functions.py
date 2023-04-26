import string
from datetime import datetime
from random import choice

from src.database.database_context import Semester


def get_current_semester():
    now = datetime.now()
    semester = Semester.query.filter(Semester.start_date <= now, Semester.end_date >= now).first()
    return semester.id


def gen_digits(max_length):
    return str(''.join(choice(string.digits) for i in range(max_length)))
