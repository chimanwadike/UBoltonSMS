from flask import Blueprint, request
from src.services.timetable_service import get_course_schedules
from flasgger import swag_from

schedules = Blueprint("schedules", __name__, url_prefix="/api/v1/schedules")


@schedules.get('/')
@swag_from('../docs/schedules/get_all.yaml')
def get_schedules():
    return get_course_schedules(request.args)
