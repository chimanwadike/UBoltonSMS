from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, User
import validators
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token


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

    user = User(first_name=fName, last_name=lName, email=email, phone_number=pNumber, password=pword_hash)
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
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return jsonify({
                'user': {
                    'refresh_token': refresh,
                    'access_token': access,
                    'email': user.email
                }
            }), HTTP_200_OK

        return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED
