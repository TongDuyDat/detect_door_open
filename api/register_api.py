from flask import Blueprint
from api.live_stream import live

api = Blueprint("api", __name__, url_prefix="/")

api.register_blueprint(live, url_prefix='/api')
