#!/usr/bin/python3
""" Module initializing the app instance """
import os
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)

# link the blueprint to the app (FLask obj)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close_db(exc):
    """Close the db session"""
    storage.close()


if __name__ == "__main__":
    host_d = os.getenv("HBNB_API_HOST") or "0.0.0.0"
    port_d = os.getenv("HBNB_API_PORT") or 5000
    app.run(host=host_d, port=5000, threaded=True)
