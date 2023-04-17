# Import the seed functions from seed_data.py
from src.database.database_seeder import seed_users, seed_roles, seed_courses, seed_semesters, seed_venues, seed_lecture_schedules

def seed_all():
    seed_users()
    seed_roles()
    seed_courses()
    seed_semesters()
    seed_venues()
    seed_lecture_schedules()

# # Call the seed_all() function to run all the seed functions at once
# seed_all()
