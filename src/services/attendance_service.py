import random
import string
from datetime import datetime

from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, LectureSession, TutorCourseAssignment
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity