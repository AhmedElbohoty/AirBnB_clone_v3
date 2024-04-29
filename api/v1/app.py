#!/usr/bin/python3
""" The app v1"""

from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handle not found page """
    status = {"error": "Not found"}
    return jsonify(status), 404


if __name__ == '__main__':
    try:
        host = getenv('HBNB_API_HOST')
        port = getenv('HBNB_API_PORT')
    except Exception:
        host = '0.0.0.0'
        port = '5000'

    app.run(host=host, port=port)
