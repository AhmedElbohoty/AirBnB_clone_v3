#!/usr/bin/python3
""" View for Amenities """
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Get all Amenity objects """
    # Get all objects from storage
    amenities = storage.all(Amenity).values()
    res = [obj.to_dict() for obj in amenities]

    return jsonify(res)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_get(amenity_id):
    """ Get amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id):
    """ Delete amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities/', methods=['POST'],
                 strict_slashes=False)
def create_amenity():
    """ Create amenity """
    # Handle request body
    body = request.get_json()
    if body is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    amenity = Amenity(**body)
    amenity.save()

    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """ handles PUT method """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    # Handle request body
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    for k, v in body.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(amenity, k, v)

    storage.save()

    return jsonify(amenity.to_dict()), 200
