#!/usr/bin/python3
"""Module contains routes for review resource"""

from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from api.v1.views import app_views


class_name = "Review"


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def fetch_place_reviews(place_id):
    """Returns all reviews for a place"""

    res = storage.get(Place, place_id)
    if not res:
        abort(404)

    reviews = res.reviews

    all_reviews = [review.to_dict() for review in reviews]
    return jsonify(all_reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def fetch_review(review_id):
    """Returns a review given an id"""

    res = storage.get(Review, review_id)
    if not res:
        abort(404)

    return jsonify(res)


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False,
                 methods=["POST"])
def create_place_review(place_id):
    """creates a review for a place in the database"""

    place = storage.get(Place, place_id)
    if not place:
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

    if "text" not in req_data:
        abort(400, "Missing text")

    attribs = {**req_data, "place_id": place_id}
    new_review = Review(**attribs)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """deletes a review"""
    obj = storage.get(Review, review_id)
    if not obj:
        return abort(404)

    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    """updates data for a review"""

    if request.headers.get('Content-Type') != 'application/json':
        abort(400, "Not a JSON")

    obj = storage.get(Review, review_id)
    if not obj:
        return abort(404)

    req_data = request.get_json()
    if not req_data:
        return abort(400, "Not a JSON")

    for key, val in req_data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(obj, key, val)
    obj.save()
    storage.reload()
    updated = storage.get(Review, review_id)
    return jsonify(updated.to_dict()), 200
