#!/usr/bin/python3
""" Module containing all routes belonging to app_views"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.engine.db_storage import classes


@app_views.route("/status")
def index():
    """
    returns a JSON message
    """
    message = {"status": "OK"}
    return jsonify(message)


@app_views.route("/stats")
def stats():
    """
    retrieves the number of each objects by type
    """
    output = {}
    for key, val in classes.items():
        if key == "Amenity":
            output["amenities"] = storage.count(val)
        if key == "City":
            output["cities"] = storage.count(val)
        if key == "Place":
            output["places"] = storage.count(val)
        if key == "Review":
            output["reviews"] = storage.count(val)
        if key == "State":
            output["states"] = storage.count(val)
        if key == "User":
            output["users"] = storage.count(val)
    return jsonify(output)
