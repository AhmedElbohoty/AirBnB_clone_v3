#!/usr/bin/python3
"""
View for States that handles all RESTful API actions
"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_all():
    """ Returns list of all State objects """
    # Get all states from storage
    values = storage.all("State").values()

    states = []
    for state in values:
        states.append(state.to_json())
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def state_get(state_id):
    """ Get state by id """
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    return jsonify(state.to_json())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def state_delete(state_id):
    """ Delete state by id """
    state = storage.get("State", state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def state_post():
    """ Create new states """
    # Handle request body
    data = request.get_json()

    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    state = State(**data)
    state.save()

    return jsonify(state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def state_put(state_id):
    """ Update state """
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    # Handle request body
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        ignore_keys = ["id", "created_at", "updated_at"]
        if key not in ignore_keys:
            state.bm_update(key, value)

    state.save()

    return jsonify(state.to_json()), 200
