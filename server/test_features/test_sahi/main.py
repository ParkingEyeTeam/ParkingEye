# import streamlit as st
import time

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


image = Image.open('test.jpg')

# perform prediction

detection_model = get_model()
# detection_model = Yolov5DetectionModel(
#     model_path=yolov5_model_path,
#     confidence_threshold=0.3,
#     device="cuda:0",  # or 'cuda:0'
# )
image_size = 416

all_time = 0
for i in range(10):
    t = time.time()
    if i >= 2:
        result = get_sliced_prediction(
            image,
            detection_model,
            # slice_width=256,
            # slice_height=256
        )
        # result = get_prediction(image, detection_model)
        all_time += time.time() - t
print(all_time / 8)
result.export_visuals(export_dir="demo_data/")
