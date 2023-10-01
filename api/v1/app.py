#!/usr/bin/python3
"""This contains our flask app"""

from flask import Flask, jsonify, make_response
from models import storage
from flask_cors import CORS
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)

app = Flask(__name__)
"""creates a CORS instance allowing: /* for 0.0.0.0"""
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})

@app.teardown_appcontext
def teardown(exception=None):
    """This removes the SQLAlchemy current session"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """Handle all not found errors"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", 5000)
    app.run(host=host, port=port, threaded=True, debug=True)
