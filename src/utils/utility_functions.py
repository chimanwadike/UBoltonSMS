from datetime import datetime

from src.database.database_context import Semester


def get_current_semester():
    now = datetime.now()
    semester = Semester.query.filter(Semester.start_date <= now, Semester.end_date >= now).first()
    return semester.id
