from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, User, Role
import validators
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, verify_jwt_in_request

from src.utils.utility_functions import gen_digits


# register user
def create_user(self):
    data = self.get_json()

    email = data.get('email', '')
    fName = data.get('first_name', '')
    lName = data.get('last_name', '')
    pNumber = data.get('phone_number', '')
    pword = data.get('password', '')

    if not validators.email(email):
        return jsonify({'error_message': 'The email is invalid'}), \
            HTTP_400_BAD_REQUEST

    user_exist = User.query \
        .filter(User.email == email).first()

    if user_exist:
        return jsonify({'error_message': 'A user with the same email already exists'}), \
            HTTP_409_CONFLICT

    pword_hash = generate_password_hash(pword)

    user = User(first_name=fName, last_name=lName, email=email, phone_number=pNumber, password=pword_hash,
                user_code=gen_digits(7))
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User Registered Succesfully',
        'user': {'id': user.id,
                 'first_name': user.first_name,
                 'last_name': user.last_name,
                 'phone_number': user.phone_number,
                 'email': user.email,
                 'status': user.status
                 }
    }), HTTP_201_CREATED


def authenticate(args):
    data = args.get_json()
    email = data.get('email', '')
    password = data.get('password', '')

    user = User.query.filter_by(email=email).first()

    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            roles = [role.to_dict()['id'] for role in user.roles]
            is_admin = 1 in roles
            is_student = 2 in roles
            is_tutor = 3 in roles

            # user.roles.query.filter(Role.id)
            more_claims = {"is_admin": is_admin, "is_student": is_student, "is_tutor": is_tutor}
            refresh = create_refresh_token(identity=user.id, additional_claims=more_claims)
            access = create_access_token(identity=user.id, additional_claims=more_claims)

            return jsonify({
                'user': {
                    'refresh_token': refresh,
                    'access_token': access,
                    'email': user.email,
                    'claims': more_claims
                }
            }), HTTP_200_OK
        else:
            return jsonify({'error': 'Incorrect password'}), HTTP_400_BAD_REQUEST

    return jsonify({'error': 'User with the email not found'}), HTTP_404_NOT_FOUND


def token_refresh(args):
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    if user_id:
        access_token = create_access_token(identity=user_id)
        return jsonify({'access_token': access_token}), HTTP_200_OK
    return jsonify({'error': 'Identity error encountered'}), HTTP_400_BAD_REQUEST
