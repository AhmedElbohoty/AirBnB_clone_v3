#!/usr/bin/python3
"""
View for Reviews
"""


from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """ Get all reviews """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = [obj.to_dict() for obj in place.reviews]

    return jsonify(res)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """ Get review """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete review """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    review.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    # Handle request body
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'user_id' not in body:
        abort(400, "Missing user_id")
    if 'text' not in body:
        abort(400, "Missing text")

    user = storage.get(User, body['user_id'])
    if user is None:
        abort(404)

    review = Review(**body)
    review.place_id = place_id
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def review_put(review_id):
    """ Update review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    # Handle request body
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    for k, v in body.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(review, k, v)

    storage.save()

    return jsonify(review.to_dict()), 200
