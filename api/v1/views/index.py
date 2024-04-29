#!/usr/bin/python3
""" Index page """

from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})
