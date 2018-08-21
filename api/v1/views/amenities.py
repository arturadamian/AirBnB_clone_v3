#!/usr/bin/python3
"""Create Amenity objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import Amenity


@app_views.route("/amenities", methods=["GET"])
def get_all_amenities():
    """Retrieves the list of all Amenity objects
    Return:
        jsonified version of the amenities list
    """
    amenity_list = []
    for value in storage.all("Amenity").values():
        amenity_list.append(value.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<uuid:amenity_id>", methods=["GET"])
def get_amenity_object(amenity_id):
    """Retrieves a Amenity object
    Args:
        amenity_id: id of the amenity in uuid format
    Return:
        jsonified version of the amenity object
    """
    try:
        return jsonify(storage.get("Amenity", amenity_id).to_dict())
    except Exception:
        abort(404)


@app_views.route("/amenities/<uuid:amenity_id>", methods=["DELETE"])
def delete_amenity_object(amenity_id):
    """Deletes a Amenity object
    Args:
        amenity_id: id of the amenity in uuid format
    Return:
        jsonified version of empty dictionary with status code 200
    """
    try:
        storage.delete(storage.get("Amenity", amenity_id))
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/amenities", methods=["POST"])
def post_amenity():
    """Creates a amenity object
    Returns:
        jsonified version of created amenity object
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    amenity_dict = request.get_json()
    if "name" not in amenity_dict:
        return jsonify({"error": "Missing name"}), 400
    else:
        a_name = amenity_dict["name"]
        amenity = Amenity(name=a_name)
        for key, value in amenity_dict.items():
            setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<uuid:amenity_id>", methods=["PUT"])
def put_amenity(amenity_id):
    """Updates a Amenity object
    Args:
        amenity_id: id of the amenity in uuid format
    Returns:
        jsonified version of updates amenity
    """
    ignore = ["id", "created_at", "updated_at"]
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    json = request.get_json()
    for key, value in json.items():
        if key not in ignore:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
