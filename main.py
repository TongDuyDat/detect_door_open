from flask import Flask, Response, request, url_for, send_from_directory, send_file, render_template
import cv2
from flask_cors import CORS
from api.config import Config
import time, os
app = Flask(__name__, static_folder='static')
app.config.from_object(Config)
ROOT = os.path.dirname(__file__)
CORS(app)
from api.register_api import api

if __name__ == '__main__':
    app.register_blueprint(api)
    app.run(debug=True, port=5000, threaded=True)