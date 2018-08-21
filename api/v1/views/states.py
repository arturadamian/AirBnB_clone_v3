#!/usr/bin/python3
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort

@app_views.route("/states", methods=["GET"])
def grab_states():
    """
    Retrieves a list of states
    Return:
        a list of objects
    """
    state_list=[]
    for k, v in storage.all("State").items():
        state_list.append(v.to_dict())
    return jsonify(state_list)
