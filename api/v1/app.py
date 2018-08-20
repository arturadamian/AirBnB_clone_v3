#!/usr/bin/python3
"""
Creates a blueprint for flask
"""
from models import storage, Blueprint
from api.v1.views import app_views
from flask import Flask


app = Flask(__name__)
app_views = Blueprint('app_views', __name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(self):
    """
    Created teardown for closing storage
    """
    storage.close()


if __name__ == "__main__":
    """
    sets the port and host name depending on input
    """
    if HBNB_API_HOST is not None:
        hosts = HBNB_API_HOST
    else:
        hosts = '0.0.0.0'

    if HBNB_API_PORT is not None:
        ports = HBNB_API_PORT
    else:
        ports = 5000
    app.run(host=hosts, port=ports, threaded=True)
