#!/usr/bin/python3
"""Module contains routes for amenity resource"""

from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


class_name = "Amenity"


@app_views.route("/amenities", strict_slashes=False)
def fetch_all_amenities():
    """Returns all amenities
    """
    db_response = storage.all(class_name)
    all_amenities = [amenity.to_dict() for amenity in db_response.values()]
    return all_amenities


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """creates a amenity in the database"""
    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    req_data = request.get_json()
    if req_data is None:
        abort(400, "Not a JSON")

    if "name" not in req_data:
        abort(400, "Missing name")
    new_amenity = Amenity(name=req_data.get("name"))
    new_amenity.save()
    return new_amenity.to_dict(), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["GET"])
def fetch_amenity(amenity_id):
    """returns data for a single amenity"""
    res = storage.get(Amenity, amenity_id)
    if not res:
        abort(404)

    return jsonify(res.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """deletes data for a single amenity"""
    obj = storage.get(Amenity, amenity_id)
    if not obj:
        return abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id):
    """updates data for a state"""

    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    obj = storage.get(Amenity, amenity_id)
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
    updated = storage.get(Amenity, amenity_id)
    return jsonify(updated.to_dict()), 200
