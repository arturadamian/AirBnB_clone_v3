#!/usr/bin/python3
"""creates a route"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import City


@app_views.route("/states/<uuid:state_id>/cities", methods=["GET"])
def get_all_cities_by_sate(state_id):
    """Retrieves the list of all City objects of a State
    Args:
        state_id: id of the state in uuid format
    Return:
        jsonified version of the city list
    """
    if storage.get("State", state_id) is None:
        abort(404)
    city_list = []
    for key, value in storage.all("City").items():
        if value.state_id == str(state_id):
            city_list.append(value.to_dict())
    return jsonify(city_list)


@app_views.route("/cities/<uuid:city_id>", methods=["GET"])
def get_city_object(city_id):
    """Retrieves a City object
    Args:
        city_id: id of the city in uuid format
    Return:
        jsonified version of the city object
    """
    try:
        return jsonify(storage.get("City", city_id).to_dict())
    except Exception:
        abort(404)


@app_views.route("/cities/<uuid:city_id>", methods=["DELETE"])
def delete_city_object(city_id):
    """Deletes a City object
    Args:
        city_id: id of the city in uuid format
    Return:
        jsonified version of empty dictionary with status code 200
    """
    try:
        storage.delete(storage.get("City", city_id))
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/states/<uuid:state_id>/cities", methods=["POST"])
def post_city(state_id):
    """Creates a City
    Args:
        state_id: id of the state in uuid format
    Returns:
        jsonified version of created city
    """
    if storage.get("State", state_id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    city_dict = request.get_json()
    if "name" not in city_dict:
        return jsonify({"error": "Missing name"}), 400
    else:
        c_name = city_dict["name"]
        city = City(name=c_name, state_id=state_id)
        for key, value in city_dict.items():
            setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 201


@app_views.route("/cities/<uuid:city_id>", methods=["PUT"])
def put_city(city_id):
    """Updates a City object
    Args:
        city_id: id of the city in uuid format
    Returns:
        jsonified version of updates city
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    json = request.json
    for key, value in json.items():
        if key != "id" and key != "created_at" and key != "updated_at":
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
