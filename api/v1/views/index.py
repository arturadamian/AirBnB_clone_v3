#!/usr/bin/python3
"""creates a route"""
from api.v1.views import app_views
from flask import jsonify
import models


@app_views.route("/status")
def status():
    """return status in json"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type:"""
    stat_dict = {"amenities": 0,
                 "cities": 0,
                 "places": 0,
                 "reviews": 0,
                 "states": 0,
                 "users": 0}
    name_dict = {"Amenity": "amenities",
                  "City": "cities",
                  "Place": "places",
                  "Review": "reviews",
                  "State": "states",
                  "User": "users"}
    for obj in name_dict:
        try:
            stat_dict[name_dict[obj]] = models.storage.count(
                models.classes(obj))
        except Exception:
            continue
    return jsonify(stat_dict)
