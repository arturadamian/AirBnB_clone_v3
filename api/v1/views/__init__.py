#!/usr/bin/python3
"""creating package"""
from flask import Blueprint

<<<<<<< HEAD
=======
# Do not move, need Blueprint instantiated before the import all or it
# will fail
>>>>>>> c6a80ad9c6589671d8ab682078e946bb7f165ad2
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
<<<<<<< HEAD
from api.v1.views.amenities import *
=======
>>>>>>> c6a80ad9c6589671d8ab682078e946bb7f165ad2
