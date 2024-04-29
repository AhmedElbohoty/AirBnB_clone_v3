#!/usr/bin/python3
"""
View for Places
"""


from flask import jsonify, request, abort
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ Get all Places related to City """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    # Get all values
    values = storage.all("Place").values()

    places = []
    for place in values:
        if place.city_id == city_id:
            places.append(place.to_dict())

    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """ Get place """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place = place.to_dict()
    return jsonify(place)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """ Delete place """

    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create place """
    city = storage.get("City", city_id)
    if city is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data.keys():
        abort(400, "Missing user_id")

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data.keys():
        abort(400, "Missing name")

    place = Place(**data)
    place.city_id = city_id
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """ handles PUT method """
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")

    for key, value in data.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            place.update(key, value)
    place.save()

    return jsonify(place.to_dict()), 200
