from io import BytesIO
import cv2, time
import torch
from flask import Response
from flask import Blueprint, request
from yolov5.detect import run, detect_img
from api.config import Config
from  PIL import Image
import pathlib

from yolov5.models.common import DetectMultiBackend
from yolov5.models.experimental import attempt_load
from yolov5.utils.torch_utils import select_device
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
live = Blueprint('live', __name__, url_prefix="/api")

# model = torch.hub.load(Config.YOLOv5, 'custom', path=Config.WEIGHTS, source='local',classes=2, channels = 3, pretrained = True, force_reload=True)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = select_device(device)
model = attempt_load(Config.WEIGHTS, device=device)
def generate_frames():
    url = "D:/ThucTap/Class_detect/data/IMG_2929.MP4"
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    while True:
        success, frame = camera.read()
        frame = cv2.flip(frame,1)
        if not success:
            break
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        time.sleep(.1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
def detect(step = 1):
    path = "D:/freelance/detect_door_open/Datatest.mp4"
    camera = cv2.VideoCapture(0)
    count = 0
    while True:
        success, frame = camera.read()
        # frame = cv2.flip(frame,1)
        if not success:
            break
        im0 = frame
        if count%step == 0:   
            im0, _= detect_img(frame, model)
            im0 = cv2.resize(im0, dsize=(frame.shape[1], frame.shape[0]) )
        _, buffer = cv2.imencode('.jpg', im0)
        frame_data = buffer.tobytes()
        time.sleep(.01)
        count+=1
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
@live.route('/live/')
def video_stream():
    ai = request.args.get("ai")
    print(ai)
    if ai:
        return Response(detect(1), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    