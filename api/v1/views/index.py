#!/usr/bin/python3
"""creates a route"""
from api.v1.views import app_views
from flask import jsonify


@app_view.route("/status")
def staus():
    """return status in json"""
    return jsonify({"status": "OK" })
