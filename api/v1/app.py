#!/usr/bin/python3
"""
Creates a blueprint for flask
"""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
import os
from flask_cors import CORS


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.url_map.strict_slashes = False
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """
    Created teardown for closing storage
    """
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """
    404 error page in JSON
    """
    return jsonify({"error": "Not Found"}), 404


if __name__ == "__main__":
    """
    sets the port and host name depending on input
    """
    hosts = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(os.getenv("HBNB_API_PORT", default=5000))
    app.run(host=hosts, port=ports, threaded=True)
