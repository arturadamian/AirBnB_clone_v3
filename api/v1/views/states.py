#!/usr/bin/python3
"""
This file contains the api routes for states
"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import State


@app_views.route("/states", methods=["GET"])
def grab_states():
    """
    Retrieves a list of states
    Return:
        a list of objects
    """
    state_list = []
    for v in storage.all("State").values():
        state_list.append(v.to_dict())
    return jsonify(state_list)


@app_views.route("/states/<state_id>", methods=["GET"])
def grab_state(state_id):
    """
    Retrieves a certain State
    Args:
        state_id: id of the state needed
    Return:
        jasonified dictionary of the state
    """
    all_states = storage.all("State")
    full_id = "State." + state_id
    try:
        indiv = all_states.get(full_id).to_dict()
        return jsonify(indiv)
    except Exception:
        abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def state_go_poof(state_id):
    """
    Deletes a certain State
    Args:
        state_id: id of the state needed
    Return:
        empty dictionary or 404 error
    """
    all_states = storage.all("State")
    full_id = "State." + state_id
    try:
        indiv = all_states.get(full_id)
        indiv.delete()
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/states", methods=["POST"])
def posting_states():
    """
    Creating a new state object
    Return:
        jsonified dicitonary of the new object or error 400 and 404
    """
    try:
        if not request.json:
            return jsonify({"error": "Not a JSON"}), 400
        data = request.get_json()
        if "name" not in data:
            return jsonify({"error": "Missing name"}), 400
        new_obj = State(name=data["name"])
        new_obj.save()
        return jsonify(new_obj.to_dict()), 201
    except Exception:
        abort(404)


@app_views.route("/states/<state_id>", methods=["PUT"])
def alter_state(state_id):
    """
    alters an existing State object
    Args:
        state_id: id of the state needed
    Return:
        jsonified dictionary of the object or errors 400 and 404
    """
    ignore = {"id", "created_at", "updated_at"}
    indiv = storage.get("State", state_id)
    if indiv is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(indiv, key, value)
    return jsonify(indiv.to_dict()), 200
