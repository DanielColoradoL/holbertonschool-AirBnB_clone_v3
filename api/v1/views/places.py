#!/usr/bin/python3
"""Module contains routes for state resource"""

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


class_name = "Place"


@app_views.route("/places", strict_slashes=False)
def fetch_all_places():
    """Returns all places"""
    db_response = storage.all(class_name)
    all_places = [place.to_dict() for place in db_response.values()]
    return jsonify(all_places)


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def fetch_all_places(city_id):
    """Returns all places"""

    res = storage.get(City, city_id)
    if not res:
        abort(404)

    places = res.places

    all_places = [place.to_dict() for place in places]
    return jsonify(all_places)


@app_views.route("/<city_id>/places", strict_slashes=False, methods=["POST"])
def create_place(city_id):
    """creates a place in the database"""

    city_id = req_data.get("city_id")
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    req_data = request.get_json()
    if req_data is None:
        abort(400, "Not a JSON")

    if "user_id" not in req_data:
        abort(400, "Missing user_id")

    user = storage.get(User, req_data["user_id"])
    if not user:
        abort(404)

    if "name" not in req_data:
        abort(400, "Missing name")

    new_place = Place(**req_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def fetch_place(place_id):
    """returns data for a single place"""
    res = storage.get(Place, place_id)
    if not res:
        abort(404)

    return jsonify(res.to_dict())


@app_views.route("/places/<place_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """deletes data for a single place"""
    obj = storage.get(Place, place_id)
    if not obj:
        return abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_state(place_id):
    """updates data for a state"""

    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    obj = storage.get(Place, place_id)
    if not obj:
        return abort(404)

    req_data = request.get_json()
    if not req_data:
        return abort(400, "Not a JSON")

    for key, val in req_data.items():
        if key not in ["id", "user_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(obj, key, val)
    obj.save()
    storage.reload()
    updated = storage.get(Place, place_id)
    return jsonify(updated.to_dict()), 200
