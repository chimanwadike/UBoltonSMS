from flask import Blueprint, request
from src.services.semester_service import create_semester, get_semesters

semesters = Blueprint("semesters", __name__, url_prefix="/api/v1/semesters")


@semesters.get('/')
def get_all():
    return get_semesters()


@semesters.post('/')
def create():
    return create_semester(request.get_json())
