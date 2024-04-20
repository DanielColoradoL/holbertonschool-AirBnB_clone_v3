#!/usr/bin/python3
"""Module contains routes for user resource"""

from flask import jsonify, abort, request
from models import storage
from models.user import User
from api.v1.views import app_views


class_name = "User"


@app_views.route("/users", strict_slashes=False)
def fetch_all_users():
    """Returns all users
    """
    db_response = storage.all(class_name)
    all_users = [user.to_dict() for user in db_response.values()]
    return all_users


@app_views.route("/users", strict_slashes=False, methods=["POST"])
def create_user():
    """creates a user in the database"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    req_data = request.get_json()
    if req_data is None:
        abort(400, "Not a JSON")

    attribs = {}

    if "email" not in req_data:
        abort(400, "Missing email")
    else:
        attribs["email"] = req_data["email"]

    if "password" not in req_data:
        abort(400, "Missing password")
    else:
        attribs["password"] = req_data["password"]

    if "first_name" in req_data:
        attribs["first_name"] = req_data["first_name"]

    if "last_name" in req_data:
        attribs["last_name"] = req_data["last_name"]

    new_user = User(**attribs)
    new_user.save()
    return new_user.to_dict(), 201


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=["GET"])
def fetch_user(user_id):
    """returns data for a single user"""
    res = storage.get(User, user_id)
    if not res:
        abort(404)

    return jsonify(res.to_dict())


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_user(user_id):
    """deletes data for a single user"""
    obj = storage.get(User, user_id)
    if not obj:
        return abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/<user_id>",
                 strict_slashes=False,
                 methods=["PUT"])
def update_user(user_id):
    """updates data for a state"""

    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    obj = storage.get(User, user_id)
    if not obj:
        return abort(404)

    req_data = request.get_json()
    if not req_data:
        return abort(400, "Not a JSON")

    for key, val in req_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, key, val)
    obj.save()
    storage.reload()
    updated = storage.get(User, user_id)
    return jsonify(updated.to_dict()), 200
