#!/usr/bin/python3
"""Create Place objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import Place


@app_views.route("/cities/<uuid:city_id>/places", methods=["GET"])
def get_all_place_by_city(city_id):
    """Retrieves the list of all Place objects of a City
    Args:
        city_id: id of the city in uuid format
    Return:
        jsonified version of the place list
    """
    if storage.get("City", city_id) is None:
        abort(404)
    place_list = []
    for key, value in storage.all("Place").items():
        if value.city_id == str(city_id):
            place_list.append(value.to_dict())
    return jsonify(place_list)


@app_views.route("/places/<uuid:place_id>", methods=["GET"])
def get_place_object(place_id):
    """Retrieves a Place object
    Args:
        place_id: id of the place in uuid format
    Return:
        jsonified version of the place object
    """
    try:
        return jsonify(storage.get("Place", place_id).to_dict())
    except Exception:
        abort(404)


@app_views.route("/places/<uuid:place_id>", methods=["DELETE"])
def delete_place_object(place_id):
    """Deletes a Place object
    Args:
        place_id: id of the place in uuid format
    Return:
        jsonified version of empty dictionary with status code 200
    """
    try:
        storage.delete(storage.get("Place", place_id))
        storage.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("/cities/<uuid:city_id>/places", methods=["POST"])
def post_place(city_id):
    """Creates a Place
    Args:
        city_id: id of the city in uuid format
    Returns:
        jsonified version of created place
    """
    if storage.get("City", city_id) is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    place_dict = request.get_json()
    if "user_id" not in place_dict:
        return jsonify({"error": "Missing user_id"}), 400
    if storage.get("User", place_dict["user_id"]) is None:
        abort(404)
    if "name" not in place_dict:
        return jsonify({"error": "Missing name"}), 400
    else:
        p_user_id = place_dict["user_id"]
        p_name = place_dict["name"]
        place = Place(user_id=p_user_id, name=p_name, city_id=city_id)
        for key, value in place_dict.items():
            setattr(place, key, value)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<uuid:place_id>", methods=["PUT"])
def put_place(place_id):
    """Updates a Place object
    Args:
        place_id: id of the place in uuid format
    Returns:
        jsonified version of updates place
    """
    ignore = ["id", "city_id", "user_id", "created_at", "updated_at"]
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    json = request.get_json()
    for key, value in json.items():
        if key not in ignore:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=["POST"])
def get_places():
    """
    gets a list of all places requested
    """
    temp_place = set()
    place_list = []
    try:
        if request.get_json() is None:
            return jsonify({'error': 'Not a JSON'}), 400
        json = request.get_json()
        all_states = json.get("states", [])
        all_cities = json.get("cities", [])
        if all_states == [] and all_cities == []:
            for indiv_place in storage.all("Place").values():
                temp_place.add(indiv_place)
        json = request.get_json()
        if all_states != []:
            for indiv in all_states:
                state_indiv = storage.get("State", indiv)
                temp_cities = state_indiv.cities
                for indiv_city in temp_cities:
                    for indiv_place in indiv_city.places:
                        temp_place.add(indiv_place)
        if all_cities != []:
            for indiv in all_cities:
                city_indiv = storage.get("City", indiv)
                for indiv_place in city_indiv.places:
                    temp_place.add(indiv_place)

        all_amenities = json.get("amenities", [])
        if all_amenities != []:
            all_amen_obj = set()
            temp_copy = temp_place.copy()
            for indiv in all_amenities:
                all_amen_obj.add(storage.get("Amenity", indiv))
            for indiv_places in temp_copy:
                amenities = indiv_places.amenities
                for indiv_amen in amenities:
                    if indiv_amen not in all_amen_obj:
                        temp_place.discard(indiv_places)
                        break
        for indiv in temp_place:
            place_list.append(indiv.to_dict())
    except Exception:
        return jsonify({'error': 'Not a JSON'}), 400
    return jsonify(place_list)
