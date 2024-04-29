#!/usr/bin/python3
"""
View for Places
"""


from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from models.state import State
from api.v1.views import app_views


@app_views.route('/cities/<string:city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """ Get all Places related to City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = [obj.to_dict() for obj in city.places]

    return jsonify(res)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ Get place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ Delete place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()

    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ Create place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    # Handle request body
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'user_id' not in body:
        abort(400, "Missing user_id")
    if 'name' not in body:
        abort(400, "Missing name")

    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)

    place = Place(**body)
    place.city_id = city_id
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ handles PUT method """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # Handle request body
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    for k, v in body.items():
        ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(place, k, v)

    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_places_id():
    """ Search places by id """

    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    states = body.get('states', [])
    cities = body.get('cities', [])
    amenities = body.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        places = set()

        for s_id in states:
            state = storage.get(State, s_id)
            if state:
                places.update(
                    place for city in state.cities for place in city.places)

        for c_id in cities:
            city = storage.get(City, c_id)
            if city:
                places.update(city.places)

        if amenities:
            places = set(storage.all(Place).values())
            amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
            places = [place for place in places if all(
                am in place.amenities for am in amenities_obj)]

    places_data = []
    for place in places:
        place_data = place.to_dict()
        place_data.pop('amenities', None)
        places_data.append(place_data)

    return jsonify(places_data)
