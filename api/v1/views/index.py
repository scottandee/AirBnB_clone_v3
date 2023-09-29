#!/usr/bin/python3
"""Routes in the blueprint"""

from api.v1.views import app_views
from flask import jsonify, make_response
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage

classes = {"amenity": Amenity, "city": City,
           "place": Place, "review": Review, "state": State, "user": User}


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Returns the status as JSON"""
    return jsonify({"status": "OK"})
