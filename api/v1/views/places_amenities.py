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


@app_views.route("/places/<uuid:place_id>/amenities/<uuid:amenity_id>",
                 methods=["DELETE"])
def delete_place_amenity_object(place_id, amenity_id):
    """Deletes place_amenity object
    Args:
        place_id: id of the place in uuid format
        amenity_id: id of the amenity in uuid format
    Return:
        jsonified version of empty dictionary with status code 200
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    place_amenity = place.amenities
    place_amenity = list(amen for amen in place_amenity if
                         amen.id == amenity_id)
    print(amenity)
    print(place_amenity)
    if amenity not in place_amenity:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.remove(place_amenity[0])
    else:
        place.amenity_ids.remove(place_amenity[0].id)
    place.save()
    return jsonify({}), 200


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
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    place_amenity = place.amenities
    place_amenity = list(amen for amen in place_amenity if
                         amen.id == amenity_id)
    if place_amenity == []:
        return jsonify(amenity.to_dict()), 200
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        place.amenities.append(amenity)
    else:
        place.amenity_ids.append(amenity_id)
    place.save()
    return jsonify(amenity.to_dict()), 201
