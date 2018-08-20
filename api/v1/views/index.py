#!/usr/bin/python3
"""creates a route"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status():
    """return status in json"""
    return jsonify({"status": "OK"})
