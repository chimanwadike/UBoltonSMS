import json
from datetime import datetime

from flask import jsonify
from sqlalchemy import extract

from src.constants.http_status_codes import *
from src.database.database_context import db, Role


def get_roles(self):
    page = self.args.get('page', 1, type=int)

    per_page = self.args.get('per_page', 20, type=int)

    roles = Role.query.paginate(page=page, per_page=per_page)

    data = []
    for role in roles.items:
        data.append({'id': role.id, 'name': role.name, 'display_name': role.display_name})

    meta = {
        'page': roles.page,
        'pages': roles.pages,
        'total_count': roles.total,
        'prev_page': roles.prev_num,
        'next_page': roles.next_num,
        'has_next': roles.has_next,
        'has_prev': roles.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


def get_role(self, id):
    data = self.get_json()
    role = Role.query \
        .filter(Role.id == id) \
        .first()

    if not role:
        return jsonify({'error_message': 'Role does not exist'}), HTTP_404_NOT_FOUND

    return jsonify(
        {'id': role.id,
         'name': role.name,
         'display_name': role.display_name
         }
    ), HTTP_200_OK


def create_role(self):
    data = self.get_json()
    name = data.get('name')
    display_name = data['display_name']


    role_exist = Role.query \
        .filter(Role.display_name == display_name) \
        .filter(Role.name == name) \
        .first()

    if role_exist:
        return jsonify({'error_message': 'A role with the same name already exists'}), \
            HTTP_409_CONFLICT



    role = Role(name=name, display_name=display_name)
    db.session.add(role)
    db.session.commit()

    return jsonify(
        {'id': role.id,
         'name': role.name,
         'display_name': role.display_name
         }
    ), HTTP_201_CREATED


def delete_role(self, id):
    role = Role.query \
        .filter(Role.id == id) \
        .first()

    if not role:
        return jsonify({'message': 'Role does not exist'}), HTTP_404_NOT_FOUND

    db.session.delete(role)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT


def edit_role(self, id):
    data = self.get_json()

    role = Role.query \
        .filter(Role.id == id) \
        .first()

    if not role:
        return jsonify({'message': 'Role does not exist'}), HTTP_404_NOT_FOUND


    role.name = data['name']
    role.display_name = data['display_name']

    db.session.commit()

    return jsonify(
        {'id': role.id,
         'name': role.name,
         'display_name': role.display_name
         }
    ), HTTP_200_OK




