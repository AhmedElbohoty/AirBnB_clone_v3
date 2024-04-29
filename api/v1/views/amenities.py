#!/usr/bin/python3
"""
View for Amenities
"""


from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities_all():
    """ Get all Amenity objects """
    # Get all objects from storage
    amenities = storage.all("Amenity").values()

    objects = []
    for amenity in amenities:
        objects.append(amenity.to_dict())

    return jsonify(objects)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def amenity_get(amenity_id):
    """ Get amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def amenity_delete(amenity_id):
    """ Delete amenity """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_post():
    """ Create amenity """
    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    amenity = Amenity(**data)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_put(amenity_id):
    """ handles PUT method """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for k, v in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if k not in ignore_keys:
            amenity.update(k, v)

    amenity.save()

    return jsonify(amenity.to_dict()), 200
