# Import the seed functions from seed_data.py
from src.database.database_seeder import seed_users, seed_roles, seed_courses, seed_semesters, seed_venues, \
    seed_lecture_schedules, seed_user_roles, seed_lecture_sessions, seed_student_course_enrollment, \
    seed_lecture_schedule_student_enrolment, seed_tutor_course_enrollment


def seed_all():
    seed_users()
    seed_roles()
    seed_courses()
    seed_semesters()
    seed_venues()
    seed_lecture_schedules()
    seed_user_roles()
    seed_lecture_sessions()
    seed_lecture_schedule_student_enrolment()
    seed_student_course_enrollment()
    seed_tutor_course_enrollment()

# # Call the seed_all() function to run all the seed functions at once
# seed_all()
