from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    status = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')

    def __repr__(self) -> str:
        return 'User>>> {self.id}'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    display_name = db.Column(db.String(50), nullable=False)
    users = db.relationship('User', secondary='user_roles', back_populates='roles')


user_roles = db.Table('user_roles',
                      db.Column('id', db.Integer, primary_key=True),
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                      )


class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(15), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return 'Semester>>> {self.id}'


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    building = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self) -> str:
        return 'Venue>>> {self.id}'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'title': self.title,
            'description': self.description
        }

    def __repr__(self) -> str:
        return 'Course>>> {self.id}'

    def __repr__(self) -> str:
        return 'Role>>> {self.id}'

# class UserRole(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     role_id = db.Column(db.Integer, nullable=False)
#
#     def __repr__(self) -> str:
#         return 'UserRole>>> {self.id}'
