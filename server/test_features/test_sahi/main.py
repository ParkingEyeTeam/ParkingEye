# import streamlit as st
import time

import cv2
import sahi.utils.file
import sahi.utils.mmdet
import sahi.model
import sahi
from PIL import Image
from sahi.predict import get_prediction, get_sliced_prediction, predict
import random
# from utils import sahi_mmdet_inference
from sahi.utils.yolov5 import (
    download_yolov5s6_model,
)
from sahi.model import Yolov5DetectionModel
import torch
import gc

# from streamlit_image_comparison import image_comparison

MMDET_YOLOX_MODEL_URL = "https://download.openmmlab.com/mmdetection/v2.0/yolox/yolox_tiny_8x8_300e_coco/yolox_tiny_8x8_300e_coco_20211124_171234-b4047906.pth"
yolov5_model_path = 'models/yolov5s6.pt'
download_yolov5s6_model(destination_path=yolov5_model_path)


def get_model():
    model_path = "yolox.pt"

    sahi.utils.file.download_from_url(
        MMDET_YOLOX_MODEL_URL,
        model_path,
    )
    config_path = sahi.utils.mmdet.download_mmdet_config(
        model_name="yolox", config_file_name="yolox_tiny_8x8_300e_coco.py"
    )

    detection_model = sahi.model.MmdetDetectionModel(
        model_path=model_path,
        config_path=config_path,
        confidence_threshold=0.5,
        device="cuda:0",
    )
    return detection_model

    # visualize input image


image = Image.open('cars_test.png')
img = cv2.imread('cars_test.png')
# img = cv2.resize(img, (640, 480))
# image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# perform prediction

# detection_model = get_model()
detection_model = Yolov5DetectionModel(
    model_path=yolov5_model_path,
    confidence_threshold=0.3,
    device="cuda:0",  # or 'cuda:0'
)
# image_size = 416

all_time = 0
# model = torch.hub.load('C:\\Users\\igors/.cache\\torch\\hub\\ultralytics_yolov5_master', 'custom',
#                        'weights/yolov5m6.pt', source='local')
# model.conf = 0.4
# model.size = 1920
# gc.collect()
# torch.cuda.empty_cache()
# cv
cap = cv2.VideoCapture('13.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        # print(1)
    result = get_prediction(Image.fromarray(frame), detection_model, image_size=1920)
    for res in result.object_prediction_list:
        bbox = res.bbox.to_voc_bbox()
        # res.score
        # print(bbox)
        name = res.category.name
        cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(frame, name, (bbox[0] + 20, bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.imshow('test', frame)
    cv2.waitKey(1)