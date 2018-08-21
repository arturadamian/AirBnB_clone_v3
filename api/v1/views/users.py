#!/usr/bin/python3
"""Create User objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import User


@app_views.route("/users", methods=["GET"])
def get_all_user():
    """Retrieves the list of all User objects
    Return:
        jsonified version of the user list
    """
    user_list = []
    for value in storage.all("User").values():
        user_list.append(value.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<uuid:user_id>", methods=["GET"])
def get_user_object(user_id):
    """Retrieves a User object
    Args:
        user_id: id of the user in uuid format
    Return:
        jsonified version of the user object
    """
    try:
        return jsonify(storage.get("User", user_id).to_dict())
    except Exception:
        abort(404)


@app_views.route("/users/<uuid:user_id>", methods=["DELETE"])
def delete_user_object(user_id):
    """Deletes a User object
    Args:
        user_id: id of the user in uuid format
    Return:
        jsonified version of empty dictionary with status code 200
    """
    try:
        storage.delete(storage.get("User", user_id))
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/users", methods=["POST"])
def post_user():
    """Creates a User
    Returns:
        jsonified version of created user
    """
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    user_dict = request.get_json()
    if "email" not in user_dict:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in user_dict:
        return jsonify({"error": "Missing password"}), 400
    else:
        u_email = user_dict["email"]
        u_password = user_dict["password"]
        user = User(email=u_email, password=u_password)
        for key, value in user_dict.items():
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 201


@app_views.route("/users/<uuid:user_id>", methods=["PUT"])
def put_user(user_id):
    """Updates a User object
    Args:
        user_id: id of the user in uuid format
    Returns:
        jsonified version of updates user
    """
    ignore = ["id", "email", "created_at", "updated_at"]
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    json = request.get_json()
    for key, value in json.items():
        if key not in ignore:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
