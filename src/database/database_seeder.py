import calendar
from datetime import datetime, timedelta
from random import randint

from faker import Faker
from src.database.database_context import db, User, Role, Semester, user_roles, Venue, Course, LectureSchedule, \
    LectureSession, LectureScheduleUserEnrolment, StudentCourseEnrolment, TutorCourseAssignment
from werkzeug.security import generate_password_hash

fake = Faker()


# Seed data for User model
def seed_users():
    for _ in range(30):
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number(),
            email=fake.email(),
            password=generate_password_hash('password'),
            status='active',
            created_at=datetime.now()
        )
        db.session.add(user)
    db.session.commit()


# Seed data for Role model
def seed_roles():
    roles = [
        {'name': 'admin', 'display_name': 'Admin'},
        {'name': 'student', 'display_name': 'Student'},
        {'name': 'tutor', 'display_name': 'Tutor'}
    ]
    for role in roles:
        role_obj = Role(
            name=role['name'],
            display_name=role['display_name']
        )
        db.session.add(role_obj)
    db.session.commit()


# Seed data for Semester model
def seed_semesters():
    semesters = [
        {'name': 'First Semester', 'start_date': datetime(2023, 1, 1), 'end_date': datetime(2023, 6, 30),
         'status': 'active', 'created_at': datetime.now()},
        {'name': 'Second Semester', 'start_date': datetime(2023, 7, 1), 'end_date': datetime(2023, 8, 31),
         'status': 'active', 'created_at': datetime.now()},

    ]
    for semester in semesters:
        semester_obj = Semester(
            name=semester['name'],
            start_date=semester['start_date'],
            end_date=semester['end_date'],
            status=semester['status'],
            created_at=semester['created_at']
        )
        db.session.add(semester_obj)
    db.session.commit()


# Seed data for Venue model
def seed_venues():
    venues = [
        {'name': 'A1-001', 'building': 'Block A'},
        {'name': 'B2-002', 'building': 'Block B'},
        {'name': 'C3-003', 'building': 'Block C'}
    ]
    for venue in venues:
        venue_obj = Venue(
            name=venue['name'],
            building=venue['building']
        )
        db.session.add(venue_obj)
    db.session.commit()


# Seed data for Course model
def seed_courses():
    courses = [
        {'name': 'SWE71001', 'description': 'Software Engineering'},
        {'name': 'SWE71002', 'description': 'Advance Software Development'},
        {'name': 'SWE71002', 'description': 'DevOps'}
    ]
    for course in courses:
        course_obj = Course(
            name=course['name'],
            description=course['description'],
            created_at=datetime.now()
        )
        db.session.add(course_obj)
    db.session.commit()


# Seed data for LectureSchedule model
def seed_lecture_schedules():
    courses = Course.query.all()
    semesters = Semester.query.all()
    venues = Venue.query.all()

    for _ in range(8):
        course = fake.random_element(courses)
        semester = Semester.query.filter(Semester.id == 1).first()
        venue = fake.random_element(venues)

        start_time = fake.random_element(elements=(datetime(2023, 1, 9, 10),
                                                   datetime(2023, 1, 10, 9),
                                                   datetime(2023, 1, 11, 10),
                                                   datetime(2023, 1, 12, 9),
                                                   datetime(2023, 1, 13, 10)))
        end_time = start_time + timedelta(hours=fake.random_element(elements=(1, 3)))

        lecture_schedule = LectureSchedule(
            course_id=course.id,
            semester_id=1,  # hardcoded this value to focus seed data on current semester
            venue_id=venue.id,
            start_time=start_time,
            end_time=end_time,
            day=start_time.strftime("%A"),
            is_recurring=True,
            is_online=False,

        )
        db.session.add(lecture_schedule)

    db.session.commit()


# Seed data for user_roles association
def seed_user_roles():
    tutors = User.query.filter(User.id.in_([1, 2, 3])).all()
    tutor_roles = Role.query.filter(Role.id == 3).all()

    for user in tutors:
        user.roles.extend(tutor_roles)

    students = User.query.filter(~User.id.in_([1, 2, 3])).all()
    student_roles = Role.query.filter(Role.id == 2).all()

    for user in students:
        user.roles.extend(student_roles)

    db.session.commit()


# logic for generating checkin code in the order "AA-BB-CC"
def generate_check_in_code():
    # Generate random uppercase characters for each segment of the check-in code
    segment1 = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    segment2 = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    segment3 = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    check_in_code = f"{segment1}{segment2}{segment3}"
    return check_in_code


# Seed data for lecture_sessions association
def seed_lecture_sessions():
    # Query existing LectureSchedule objects to get their ids and start/end times
    lecture_schedules = LectureSchedule.query.all()
    # lecture_schedule_data = [(schedule.id, schedule.start_time, schedule.end_time) for schedule in lecture_schedules]

    for schedule in lecture_schedules:

        for i in range(20):  # Create 20 lecture sessions per schedule
            # lecture_schedule_id, start_time, end_time = fake.random_element(elements=lecture_schedule_data)
            allow_self_registration = fake.boolean()
            check_in_code = generate_check_in_code()  # Generate check-in code
            status = fake.random_element(elements=('active', 'completed'))
            created_at = datetime.now()

            lecture_session = LectureSession(
                lecture_schedule_id=schedule.id,
                start_time=schedule.start_time + timedelta(weeks=i),
                end_time=schedule.end_time + timedelta(weeks=i),
                allow_self_registration=allow_self_registration,
                # check_in_code=check_in_code,
                status=status,
                created_at=created_at
            )

            db.session.add(lecture_session)

    db.session.commit()


# Seed data for lecture_schedule_student_enrolment association
def seed_lecture_schedule_student_enrolment():
    # Get all users with role_id of 2 (student)
    students = User.query.join(User.roles).filter(Role.id == 2).all()

    # Loop through each student and create enrolments
    for student in students:
        enrolments = randint(1, 5)  # Randomly generate number of enrolments (1 to 5)

        for _ in range(enrolments):
            # Get a random LectureSchedule
            lecture_schedule = LectureSchedule.query.order_by(db.func.random()).first()

            # Check if the student has already been added to the lecture schedule
            existing_schedule_enrollment = LectureScheduleUserEnrolment.query.filter_by(
                user_id=student.id,
                lecture_schedule_id=lecture_schedule.id
            ).first()

            if not existing_schedule_enrollment:
                existing_course_enrolment = StudentCourseEnrolment.query.filter_by(
                    user_id=student.id,
                    course_id=lecture_schedule.course_id,
                    semester_id=lecture_schedule.semester_id
                ).first()

                if not existing_course_enrolment:
                    course_enrolment = StudentCourseEnrolment(
                        course_id=lecture_schedule.course_id,
                        user_id=student.id,
                        semester_id=lecture_schedule.semester_id
                    )

                    db.session.add(course_enrolment)

                # Create a new enrolment with lecture_schedule_id and user_id
                schedule_enrolment = LectureScheduleUserEnrolment(
                    lecture_schedule_id=lecture_schedule.id,
                    user_id=student.id
                )

                db.session.add(schedule_enrolment)

    db.session.commit()


# Seed data for tutor_course_enrollment
def seed_lecture_schedule_tutor_assignment():
    # Get all users with role_id of 3 (tutor)
    tutors = User.query.join(User.roles).filter(Role.id == 3).all()

    # Loop through each student and create enrolments
    for tutor in tutors:
        enrolments = randint(1, 5)  # Randomly generate number of enrolments (1 to 5)

        for _ in range(enrolments):
            # Get a random LectureSchedule
            lecture_schedule = LectureSchedule.query.order_by(db.func.random()).first()

            # Check if the student has already been added to the lecture schedule
            existing_schedule_assignment = LectureScheduleUserEnrolment.query.filter_by(
                user_id=tutor.id,
                lecture_schedule_id=lecture_schedule.id
            ).first()

            if not existing_schedule_assignment:
                existing_course_assignment = TutorCourseAssignment.query.filter_by(
                    user_id=tutor.id,
                    course_id=lecture_schedule.course_id,
                    semester_id=lecture_schedule.semester_id
                ).first()

                if not existing_course_assignment:
                    course_assignment = TutorCourseAssignment(
                        course_id=lecture_schedule.course_id,
                        user_id=tutor.id,
                        semester_id=lecture_schedule.semester_id
                    )

                    db.session.add(course_assignment)

                # Create a new enrolment with lecture_schedule_id and user_id
                schedule_enrolment = LectureScheduleUserEnrolment(
                    lecture_schedule_id=lecture_schedule.id,
                    user_id=tutor.id,
                    user_type='tutor'
                )

                db.session.add(schedule_enrolment)

    db.session.commit()
