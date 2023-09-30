#!/usr/bin/python3
"""Handles all the objects for amenities"""

from api.v1.views import app_views
from markupsafe import escape
from flask import jsonify, abort, make_response, request
from models.amenity import Amenity
from models import storage
from datetime import datetime


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """Return all amenities in JSON"""
    amenity_list = []
    for amenity in storage.all(Amenity).values():
        amenity_list.append(amenity.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_one_amenity(amenity_id):
    """Return the amenity with id specified as json"""
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete the amenity with specified amenity_id
    if present
    """
    amenity = storage.get(Amenity, escape(amenity_id))
    if amenity is None:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a new amenity with provided data
    in the body of the POST request
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    elif "name" not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    else:
        a = Amenity(name=request.json["name"])
        storage.new(a)
        storage.save()
        return make_response(jsonify(a.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an existing amenity with the
    provided data
    """
    if not request.is_json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    updates = request.json
    amenity = storage.get(Amenity, escape(amenity_id))
    old_amenity_dic = amenity.to_dict()

    for key in old_amenity_dic.keys():
        if key in ["created_at", "updated_at", "id"]:
            continue
        if key not in updates.keys():
            continue
        old_amenity_dic[key] = updates[key]

    new_amenity = Amenity(**old_amenity_dic)
    storage.delete(amenity)
    new_amenity.updated_at = datetime.utcnow()
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 200)
