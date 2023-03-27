from flask import jsonify
from src.constants.http_status_codes import *
from src.database.database_context import db, User
import validators
from werkzeug.security import check_password_hash, generate_password_hash


# register user
def create_user(self):
    data = self.get_json()

    email = data['email']
    fName = data['first_name']
    lName = data['last_name']
    pNumber = data['phone_number']
    pword = data['password']
    stat = data['status']

    if not validators.email(email):
        return jsonify({'error_message': 'The email is invalid'}), \
            HTTP_400_BAD_REQUEST

    user_exist = User.query \
        .filter(User.email == email).first()

    if user_exist:
        return jsonify({'error_message': 'A user with the same email already exists'}), \
            HTTP_409_CONFLICT

    pword_hash = generate_password_hash(pword)

    user = User(first_name=fName, last_name=lName, email=email, phone_number=pNumber, password=pword_hash, status=stat)
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
