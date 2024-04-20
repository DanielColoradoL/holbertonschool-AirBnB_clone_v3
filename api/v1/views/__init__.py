from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *

# defining a blueprint
app_views = Blueprint(
    "app_views",
    __name__,
    url_prefix="/api/v1")
