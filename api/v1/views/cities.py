#!/usr/bin/python3
""" Module containing all routes belonging to app_views"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"])
def all_cities_by_state(state_id):
    """
    retrieves the list of all cities by state
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route("/cities/<city_id>", methods=["GET"])
def city_by_id(city_id):
    """
    retrieves a city by city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city_by_id(city_id):
    """
    delete a city by city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"])
def post_city(state_id):
    """
    creates a city
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    try:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
        if "name" not in data.keys():
            abort(400, description="Missing name")
        data["state_id"] = state_id
        obj = City(**data)
        obj.save()
        return jsonify(obj.to_dict()), 201
    except ValueError:
        abort(400, description="Not a JSON")


@app_views.route("/cities/<city_id>", methods=["PUT"])
def update_city(city_id):
    """
    update a city
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    try:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
        if "name" not in data.keys():
            abort(400, description="Missing name")

        for key, value in data.items():
            if key in ["id", "state_id", "created_at", "updated_at"]:
                continue
            setattr(city, key, value)

        city.save()
        return jsonify(city.to_dict()), 200
    except ValueError:
        abort(400, description="Not a JSON")
