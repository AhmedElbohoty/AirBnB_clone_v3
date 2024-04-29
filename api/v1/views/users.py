#!/usr/bin/python3
"""
View for Users
"""

from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Get users """
    users = []

    users = storage.all("User").values()
    for user in users:
        users.append(user.to_dict())

    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """ Get user """
    user = storage.get("User", user_id)

    if user is None:
        abort(404)
    user = user.to_dict()

    return jsonify(user)


@app_views.route('/users/<user_id>', methods=['DELETE'])
def user_delete(user_id):
    """ Delete user """

    user = storage.get("User", user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Create user """
    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")

    user = User(**data)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def user_put(user_id):
    """ Update user """
    user = storage.get("User", user_id)

    if user is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for k, v in data.items():
        ignore_keys = ["id", "email", "created_at", "updated_at"]
        if k not in ignore_keys:
            user.update(k, v)

    user.save()

    return jsonify(user.to_dict()), 200
