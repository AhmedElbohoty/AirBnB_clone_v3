#!/usr/bin/python3
"""
View for Users - users module
"""
from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ Get users """
    users = storage.all(User).values()
    res = [obj.to_dict() for obj in users]

    return jsonify(res)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ Get user by the user id """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """ Delete user by user id """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """ Create new user """
    # Handle request body
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")
    if 'email' not in body:
        abort(400, "Missing email")
    if 'password' not in body:
        abort(400, "Missing password")

    user = User(**body)
    user.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_put(user_id):
    """ Update user """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    # Handle request body
    body = request.get_json()
    if body is None:
        abort(400, "Not a JSON")

    for k, v in body.items():
        ignore_keys = ["id", "email", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(user, k, v)

    storage.save()

    return jsonify(user.to_dict()), 200
