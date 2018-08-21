#!/usr/bin/python3
"""Create Place objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import Review


@app_views.route("/places/<uuid:place_id>/reviews", methods=["GET"])
def get_all_review_by_place(place_id):
    """Retrieves the list of all Review objects of a Place
    Args:
        place_id: id of the place in uuid format
    Return:
        jsonified version of the review list
    """
    if storage.get("Place", place_id) is None:
        abort(404)
    review_list = []
    for key, value in storage.all("Review").items():
        if value.place_id == str(place_id):
            review_list.append(value.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<uuid:review_id>", methods=["GET"])
def get_review_object(review_id):
    """Retrieves a Review object
    Args:
        review_id: id of the review in uuid format
    Return:
        jsonified version of the review object
    """
    try:
        return jsonify(storage.get("Review", review_id).to_dict())
    except Exception:
        abort(404)


@app_views.route("/reviews/<uuid:review_id>", methods=["DELETE"])
def delete_review_object(review_id):
    """Deletes a Review object
    Args:
        review_id: id of the review in uuid format
    Return:
        jsonified version of empty dictionary with status code 200
    """
    try:
        storage.delete(storage.get("Review", review_id))
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/places/<uuid:place_id>/reviews", methods=["POST"])
def post_review(place_id):
    """Creates a Review object
    Args:
        place_id: id of the place in uuid format
    Returns:
        jsonified version of created review object
    """
    if storage.get("Place", place_id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    review_dict = request.get_json()
    if "user_id" not in review_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if storage.get("User", review_dict["user_id"]) is None:
        abort(404)
    if "text" not in review_dict:
        return jsonify({"error": "Missing text"}), 400
    else:
        r_user_id = review_dict["user_id"]
        r_text = review_dict["text"]
        review = Review(user_id=r_user_id, text=r_text, place_id=place_id)
        for key, value in review_dict.items():
            setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<uuid:review_id>", methods=["PUT"])
def put_review(review_id):
    """Updates a Review object
    Args:
        review_id: id of the review in uuid format
    Returns:
        jsonified version of updates review
    """
    ignore = ["id", "place_id", "user_id", "created_at", "updated_at"]
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    json = request.get_json()
    for key, value in json.items():
        if key not in ignore:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
