from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from src.services.venue_service import create_venue, get_venues, get_venue, delete_venue, edit_venue
from flasgger import swag_from

venues = Blueprint("venues", __name__, url_prefix="/api/v1/venues")


@venues.get('/')
@swag_from('../docs/venues/get_all.yaml')
@jwt_required()
def get_all():
    return get_venues(request)


@venues.get('/<int:id>')
@swag_from('../docs/venues/get.yaml')
@jwt_required()
def get_venue_by_id(id):
    return get_venue(id)


@venues.post('/')
@swag_from('../docs/venues/create.yaml')
@jwt_required()
def create():
    return create_venue(request)


@venues.delete('/<int:id>')
@swag_from('../docs/venues/delete.yaml')
@jwt_required()
def delete(id):
    return delete_venue(request, id)


@venues.put('/<int:id>')
@venues.patch('/<int:id>')
@swag_from('../docs/venues/update.yaml')
@jwt_required()
def get(id):
    return edit_venue(request, id)
