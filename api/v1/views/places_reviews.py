#!/usr/bin/python3
"""
View for Reviews
"""


from flask import jsonify, request, abort
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """ Get all reviews """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    reviews = []
    # Get all values
    reviews = storage.all("Review").values()
    for review in reviews:
        if review.place_id == place_id:
            reviews.append(review.to_dict())

    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    """ Get review """
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """ Delete review """
    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create review """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")

    user = storage.get("User", data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        abort(400, "Missing text")

    review = Review(**data)
    review.place_id = place_id
    review.save()

    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def review_put(review_id):
    """ handles PUT method """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in ignore_keys:
            review.update(key, value)
    review.save()

    return jsonify(review.to_dict()), 200
