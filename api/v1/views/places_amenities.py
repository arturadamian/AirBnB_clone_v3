#!/usr/bin/python3
"""Create Place objects that handles all default RestFul API actions"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import Place
from models import Amenity
from os import getenv


@app_views.route("/places/<uuid:place_id>/amenities", methods=["GET"])
def get_all_amenities_by_place(place_id):
    """Retrieves the list of all Amenity objects of a Place
    Args:
        place_id: id of the place in uuid format
    Return:
        jsonified version of the amenity list
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity_list = []
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenity = place.amenities
    else:
        place_amenity = place.amenity_ids
    for amenity in place_amenity:
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity_object(place_id, amenity_id):
    """Deletes place_amenity object
    Args:
        place_id: id of the place in uuid format
        amenity_id: id of the amenity in uuid format
    Return:
        jsonified version of empty dictionary with status code 200
    """
    all_places = storage.all("Place")
    full_id_place = "Place." + place_id
    indiv_place = all_places.get(full_id_place)
    all_amenities = storage.all("Amenity")
    full_id_amenity = "Amenity." + amenity_id
    indiv_amenity = all_amenities.get(full_id_amenity)
    try:
        # place = storage.get("Place", place_id)
        # amenity = storage.get("Amenity", amenity_id)
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place_amenity = indiv_place.amenities
        else:
            place_amenity = indiv_place.amenity_ids
        place_amenity.remove(indiv_amenity)
        indiv_place.save()
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route("places/<uuid:place_id>/amenities/<uuid:amenity_id>",
                 methods=["POST"])
def post_place_amenity(place_id, amenity_id):
    """Link a Amenity object to a Place
    Args:
        place_id: id of the place in uuid format
        amenity_id: id of the amenity in uuid format
    Returns:
        jsonified version of amenity objecto
    """
    try:
        place = storage.get("Place", place_id)
        amenity = storage.get("Amenity", amenity_id)
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            place_amenity = place.amenities
        else:
            place_amenity = place.amenity_ids
        if amenity in place_amenity:
            return jsonify(amenity.to_dict()), 200
        place_amenity.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    except Exception:
        abort(404)
