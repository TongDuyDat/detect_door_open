from io import BytesIO
import os
from flask import Blueprint, request,Response, send_file, url_for
from api.config import Config
from  PIL import Image
from pathlib import Path
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
from subprocess import Popen, PIPE
records = Blueprint('records', __name__, url_prefix="/api")
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_root_path = os.path.join(root_path, Config.RECORD_PATH)
@records.route('/download_video/<filename>', methods=['GET'])
def download_video(filename):
    # Assuming your video files are stored in a folder named 'videos'
    # Adjust the folder path accordingly
    # Construct the full path to the video file
    video_path = os.path.join(save_root_path, filename)
    # Return the file as a response
    return send_file(video_path, as_attachment=True)

@records.route('/download_all_videos', methods=['GET'])
def download_all_videos():
    # Assuming your video files are stored in a folder named 'videos'
    # Adjust the folder path accordingly
    # Get a list of all files in the folder
    files = os.listdir(save_root_path)
    # Generate URLs for each file
    url = f"http://{Config.ip_address}:{Config.port}/"
    download_urls = [url + url_for('api.records.download_video', filename=f"{filename}") for filename in files]
    return download_urls