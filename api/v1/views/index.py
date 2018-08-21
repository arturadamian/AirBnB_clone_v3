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
    class_name = ["Amenity", "City", "Place", "Review", "State", "User"]
    stat_name = ["amenities", "cities", "places", "reviews", "states", "users"]
    for i in range(len(class_name)):
        try:
            stat_dict[stat_name[i]] = models.storage.count(class_name[i])
        except Exception:
            continue
    return jsonify(stat_dict)
