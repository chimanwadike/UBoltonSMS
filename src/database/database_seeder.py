from datetime import datetime, timedelta
from random import randint

from faker import Faker
from src.database.database_context import db, User, Role, Semester, Venue, Course, LectureSchedule, LectureSession, \
    lecture_schedule_student_enrolment
from werkzeug.security import generate_password_hash


fake = Faker()

# Seed data for User model
def seed_users():
    for _ in range(10):
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
        {'name': 'First Semester', 'start_date': datetime(2023, 1, 1), 'end_date': datetime(2023, 6, 30), 'status': 'active', 'created_at': datetime.now()},
        {'name': 'Second Semester', 'start_date': datetime(2023, 7, 1), 'end_date': datetime(2023, 8, 31), 'status': 'active', 'created_at': datetime.now()},

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

    for _ in range(20):
        course = fake.random_element(courses)
        semester = fake.random_element(semesters)
        venue = fake.random_element(venues)

        start_time = fake.date_time_this_decade()
        end_time = start_time + timedelta(hours=fake.random_element(elements=(1, 3)))

        lecture_schedule = LectureSchedule(
            course_id=course.id,
            semester_id=semester.id,
            venue_id=venue.id,
            day=fake.random_element(elements=('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')),
            start_time=start_time,
            end_time=end_time,
            one_off_date=fake.date_time_this_decade(),
            is_recurring=fake.boolean(),
            is_online=fake.boolean(),

        )
        db.session.add(lecture_schedule)

    db.session.commit()


def seed_user_roles():
    users = User.query.all()
    roles = Role.query.all()

    for user in users:
        # Generate a random number of roles for each user
        num_roles = fake.random_int(min=1, max=3)
        user_roles = fake.random_elements(elements=roles, unique=True, length=num_roles)
        user.roles.extend(user_roles)

    db.session.commit()


def generate_check_in_code():
    # Generate random uppercase characters for each segment of the check-in code
    segment1 = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    segment2 = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    segment3 = fake.random_uppercase_letter() + fake.random_uppercase_letter()
    check_in_code = f"{segment1}-{segment2}-{segment3}"
    return check_in_code

def seed_lecture_sessions():
    # Query existing LectureSchedule objects to get their ids
    lecture_schedules = LectureSchedule.query.all()
    lecture_schedule_ids = [schedule.id for schedule in lecture_schedules]

    for i in range(10):  # Create 10 lecture sessions
        lecture_schedule_id = fake.random_element(elements=lecture_schedule_ids)
        start_time = fake.date_time_this_decade()
        end_time = start_time + timedelta(hours=fake.random_element(elements=(1, 3)))
        allow_self_registration = fake.boolean()
        check_in_code = generate_check_in_code()  # Generate check-in code
        status = fake.random_element(elements=('active', 'completed'))
        created_at = datetime.now()

        lecture_session = LectureSession(
            lecture_schedule_id=lecture_schedule_id,
            start_time=start_time,
            end_time=end_time,
            allow_self_registration=allow_self_registration,
            check_in_code=check_in_code,
            status=status,
            created_at=created_at
        )

        db.session.add(lecture_session)

    db.session.commit()


def seed_lecture_schedule_student_enrolment():
    # Get all users with role_id of 2 (student)
    students = User.query.join(User.roles).filter(Role.id == 2).all()

    # Loop through each student and create enrolments
    for student in students:
        enrolments = randint(1, 5)  # Randomly generate number of enrolments (1 to 5)

        # Loop through each enrolment
        for _ in range(enrolments):
            # Get a random LectureSchedule
            lecture_schedule = LectureSchedule.query.order_by(db.func.random()).first()

            # Create a new enrolment with lecture_schedule_id and user_id
            enrolment = lecture_schedule_student_enrolment.insert().values(
                lecture_schedule_id=lecture_schedule.id,
                user_id=student.id
            )

            # Execute the enrolment query
            db.session.execute(enrolment)

    # Commit the changes
    db.session.commit()

# seed_users()