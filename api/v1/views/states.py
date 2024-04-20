#!/usr/bin/python3
"""Module contains routes for state resource"""

from flask import jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views


class_name = "State"

@app_views.route("/states", strict_slashes=False)
def fetch_all_states():
    """Returns all states"""
    db_response = storage.all(class_name)
    all_states = [ state.to_dict() for state in db_response.values()]
    return all_states


@app_views.route("/states", strict_slashes=False, methods=["POST"])
def create_state():
    """creates a state in the database"""
    req_data = request.get_json()
    if not req_data:
        return abort(400, "Not a JSON")
    
    state_name = req_data.get("name")
    if not state_name:
        return abort(400, "Missing name")
    
    new_state = State({"name": state_name})
    new_state.save()
    return jsonify(new_state.to_dict()), 201
    


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def fetch_state(state_id):
    """returns data for a single state"""
    res = storage.get(State, state_id)
    if not res:
        abort(404)

    return jsonify(res.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["DELETE"])
def delete_state(state_id):
    """deletes data for a single state"""
    obj = storage.get(State, state_id)
    if not obj:
        return abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>", strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    """updates data for a state"""
    obj = storage.get(State, state_id)
    if not obj:
        return abort(404)

    req_data = request.get_json()
    if not req_data:
        return abort(400, "Not a JSON")
    
    for key, val in req_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, val)
    obj.save()
    storage.reload()
    updated = storage.get(State, state_id)
    return jsonify(updated.to_dict()), 200
