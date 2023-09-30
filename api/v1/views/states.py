#!/usr/bin/python3
"""Handles all the objects for states"""

from api.v1.views import app_views
from markupsafe import escape
from flask import jsonify, abort, make_response, request
from models.state import State
from models import storage


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_states():
    """Return all states in JSON"""
    state_list = []
    for state in storage.all(State).values():
        state_list.append(state.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_one_state(state_id):
    """Return the state with id specified as json"""
    state = storage.get(State, escape(state_id))
    if state is None:
        abort(404)
    else:
        return state.to_dict()


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete the state with specified state_id
    if present
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a new state with provided data
    in the body of the POST request
    """
    if not request.is_json:
        return make_response(jsonify({"message": "Not a JSON"}), 400)
    elif "name" not in request.json:
        return make_response(jsonify({"message": "Missing name"}), 400)
    else:
        s = State(name=request.json["name"])
        storage.new(s)
        storage.save()
        return make_response(s.to_dict(), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Update an existing state with the
    provided data
    """
    if not request.is_json:
        return make_response(jsonify({"message": "Not a JSON"}), 400)

    updates = request.json
    state = storage.get(State, escape(state_id))
    old_state_dic = state.to_dict()

    for key in old_state_dic.keys():
        if key in ["created_at", "updated_at", "id"]:
            continue
        if key not in updates.keys():
            continue
        old_state_dic[key] = updates[key]

    new_state = State(**old_state_dic)
    storage.new(new_state)
    storage.delete(state)
    storage.save()
    return make_response(new_state.to_dict(), 200)
