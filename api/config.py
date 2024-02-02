class Config:
    DEBUG = True
    SECRET_KEY = 'mysecretkey' 
    DATABASE_URI = 'sqlite:///db.sqlite'
    UPLOAD_FOLDER = "video_upload"
    WEIGHTS = "D:/freelance/detect_door_open/door1.pt"
    DATASET = "yolov5/data/data.yaml"
    YOLOv5 = "D:/freelance/detect_door_open/yolov5"
    IOU_cof = 0.45
    SCORE_threshold = 0.5
    NUMBER_class = 2