#!/usr/bin/python3
"""
The endpoint (route) will be to return the status of your API:
"""
from os import getenv
from flask_cors import CORS
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_db(exception):
    """ Closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    """ Handle not found page """
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == '__main__':
    host = getenv('HBNB_API_HOST', default='0.0.0.0')
    port = getenv('HBNB_API_PORT', default='5000')

    app.run(host, int(port), threaded=True)
