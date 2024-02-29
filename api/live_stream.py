import datetime
from io import BytesIO
import os
import subprocess
import cv2, time
import torch
from flask import Response
from flask import Blueprint, request, stream_with_context
from yolov5.detect import run, detect_img
from api.config import Config
from  PIL import Image
from pathlib import Path
import pathlib
from yolov5.models.common import DetectMultiBackend
from yolov5.models.experimental import attempt_load
from yolov5.utils.torch_utils import select_device
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
from subprocess import Popen, PIPE
live = Blueprint('live', __name__, url_prefix="/api")
from threading import Lock
thread_lock = Lock()
# model = torch.hub.load(Config.YOLOv5, 'custom', path=Config.WEIGHTS, source='local',classes=2, channels = 3, pretrained = True, force_reload=True)
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = select_device(device)
model = attempt_load(Config.WEIGHTS, device=device)

rtsp_url = 'rtsp://localhost:8554/live'


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
save_root_path = os.path.join(root_path, 'record')
if os.path.exists(save_root_path) is False:
    os.makedirs(save_root_path)


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
def detect(step = 1, ai = True):
    path = "D:/freelance/detect_door_open/record/20240229105621.mp4"
    camera = cv2.VideoCapture(0)
    count = 0
    if camera:  # video
        fps = camera.get(cv2.CAP_PROP_FPS)
        w = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    else:  # stream
        fps, w, h = 30, im0.shape[1], im0.shape[0]
    save_record_path =  os.path.join(save_root_path, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    save_path = str(Path(save_record_path).with_suffix(".mp4"))  # force *.mp4 suffix on results videos
    vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"X264"), fps, (w, h))
    flag_crete_new_record = True
    while True:
        success, frame = camera.read()
        # frame = cv2.flip(frame,1)
        if not success:
            break
        im0 = frame
        if count%step == 0:   
            im0, _, clss= detect_img(frame, model, True,True)
            if 0 not in clss and flag_crete_new_record:
                save_record_path =  os.path.join(save_root_path, datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
                save_path = str(Path(save_record_path).with_suffix(".mp4"))  # force *.mp4 suffix on results videos
                vid_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
                flag_crete_new_record = False
            else:
                if 0  in clss:   # door is open
                    flag_crete_new_record = True
            im0 = cv2.resize(im0, dsize=(frame.shape[1], frame.shape[0]) )
        if not ai:
            im0 = frame
        _, buffer = cv2.imencode('.jpg', im0)
        frame_data = buffer.tobytes()
        time.sleep(.01)
        count+=1
        vid_writer.write(im0)
        cv2.waitKey(1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n')
@live.route('/live/')
def video_stream():
    ai = request.args.get("ai")
        # return Response(detect(1), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(stream_with_context(detect(1, ai)), mimetype='multipart/x-mixed-replace; boundary=frame')