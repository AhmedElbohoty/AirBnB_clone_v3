#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ Returns list of all State objects """
    # Get all states from storage
    states = storage.all(State).values()
    res = [obj.to_dict() for obj in states]

    return jsonify(res)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ Get state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Delete state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    state.delete()
    storage.save()

    return jsonify({})


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def state_post():
    """ Create new states """
    # Handle request body
    body = request.get_json()

    if body is None:
        abort(400, "Not a JSON")
    if 'name' not in body:
        abort(400, "Missing name")

    state = State(**body)
    state.save()

    return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def state_put(state_id):
    """ Update state """
    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for k, v in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if k not in ignore_keys:
            setattr(state, k, v)

    storage.save()

    return jsonify(state.to_dict()), 200
