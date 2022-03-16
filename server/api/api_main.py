import base64
import time
from typing import List
import cv2
from numpy import NaN
import torch
import sys
import os
import copy
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)

sys.path.append(parent)

from detection_module import DetectionModel
from detection_module.detection_model import ParsedResult
from fastapi import FastAPI, Response

dm = DetectionModel(device='cpu')

app = FastAPI()

@app.get("/", response_model=List[ParsedResult])
def root():
    t = time.time()
    imgPath = os.path.dirname(os.path.realpath(__file__)) + '/cars_test.png'
    img = cv2.imread(imgPath)
    ret = dm.predict(img)
    print(ret.object_prediction_list)
    print(time.time() - t)
    return DetectionModel.parse_result(ret)

@app.get(
    "/user-images/",
    responses={
        200: {
            "content": {"image": {}}
        }
    },
    response_class=Response,
    summary="Получить фото по id."
)
def get_image_by_id(
):
    imgPath = os.path.dirname(os.path.realpath(__file__)) + '/cars_test.png'
    img = cv2.imread(imgPath)
    ret = dm.predict(img)
    img_cpy = copy.deepcopy(img)
    for res in ret.object_prediction_list:
        bbox = res.bbox.to_voc_bbox()
        # res.score
        # print(bbox)
        name = res.category.name
        cv2.rectangle(img_cpy, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
        cv2.putText(img_cpy, name, (bbox[0] + 20, bbox[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    content = img_cpy.tobytes()
    return Response(encoded_img, media_type='image/jpeg')
