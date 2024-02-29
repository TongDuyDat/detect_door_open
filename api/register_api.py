from flask import Blueprint
from api.live_stream import live
from api.download_record import records
api = Blueprint("api", __name__, url_prefix="/")

api.register_blueprint(live, url_prefix='/api')
api.register_blueprint(records, url_prefix='/api')