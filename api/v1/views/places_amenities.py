#!/usr/bin/python3
""" View for Places amenities """
from flask import abort, jsonify
from models import storage
from models.amenity import Amenity
from models.place import Place
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities(place_id):
    """ Get amenities from place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    res = [obj.to_dict() for obj in place.amenities]
    return jsonify(res)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_id(place_id, amenity_id):
    """ Delete amenity """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()

    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def add_amenity(place_id, amenity_id):
    """ Add amenity to place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if amenity in place.amenities:
        return (jsonify(amenity.to_dict()), 200)

    place.amenities.append(amenity)
    storage.save()

    return (jsonify(amenity.to_dict(), 201))
