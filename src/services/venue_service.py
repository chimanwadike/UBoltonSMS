import json
from datetime import datetime

from flask import jsonify
from sqlalchemy import extract

from src.constants.http_status_codes import *
from src.database.database_context import db, Venue


def get_venues(self):
    page = self.args.get('page', 1, type=int)

    per_page = self.args.get('per_page', 5, type=int)

    venues = Venue.query.paginate(page=page, per_page=per_page)

    data = []
    for venue in venues.items:
        data.append({'id': venue.id, 'name': venue.name})

    meta = {
        'page': venues.page,
        'pages': venues.pages,
        'total_count': venues.total,
        'prev_page': venues.prev_num,
        'next_page': venues.next_num,
        'has_next': venues.has_next,
        'has_prev': venues.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), HTTP_200_OK


def get_venue(self, id):
    data = self.get_json()
    venue = Venue.query \
        .filter(Venue.id == id) \
        .first()

    if not venue:
        return jsonify({'error_message': 'Venue does not exist'}), HTTP_404_NOT_FOUND

    return jsonify(
        {'id': venue.id,
         'name': venue.name,
         'building': venue.building
         }
    ), HTTP_200_OK


def create_venue(self):
    data = self.get_json()
    name1 = data['name'],
    building = data['building']

    venue_exist = Venue.query \
        .filter(Venue.building == building) \
        .first()

    if venue_exist:
        return jsonify({'error_message': 'A venue with the same name already exists'}), \
            HTTP_409_CONFLICT



    venue = Venue(name=data.get('name'), building=building)
    db.session.add(venue)
    db.session.commit()

    return jsonify(
        {'id': venue.id,
         'name': venue.name,
         'building': venue.building
         }
    ), HTTP_201_CREATED


def delete_venue(self, id):
    venue = Venue.query \
        .filter(Venue.id == id) \
        .first()

    if not venue:
        return jsonify({'message': 'Venue does not exist'}), HTTP_404_NOT_FOUND

    db.session.delete(venue)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT


def edit_venue(self, id):
    data = self.get_json()

    venue = Venue.query \
        .filter(Venue.id == id) \
        .first()

    if not venue:
        return jsonify({'message': 'Venue does not exist'}), HTTP_404_NOT_FOUND


    venue.name = data['name']
    venue.building = data['building']

    db.session.commit()

    return jsonify(
        {'id': venue.id,
         'name': venue.name,
         'building': venue.building
         }
    ), HTTP_200_OK


