import base64
from genericpath import exists
import json
import time
from typing import List
import cv2
from numpy import NaN
from pydantic import BaseModel
import torch
import sys
import os
import pathlib
import copy
from server.detection_module import DetectionModel
from server.detection_module.detection_model import ParsedResult
from server.detection_module.drawing import MyAnnotator
import gc
import io
from starlette.responses import StreamingResponse

from fastapi import FastAPI, Response, APIRouter
gc.collect()
torch.cuda.empty_cache()
dm = DetectionModel(device='cpu')

# app = FastAPI()
router = APIRouter()

PARKING_IMGS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'parking_imgs')

def get_parking_image_url(image_id):
    apiUrl = 'http://localhost:8000/images/'
    return apiUrl + str(image_id)

class ParkingInfoResult(BaseModel):
    imgUrl: str
    address: str
    allParkingPlaces: int
    freeParkingPlaces: int

# TODO add query params: skip and geoposition
@router.get("/", response_model=ParkingInfoResult)
def root():
    # Require an existing cars_test.png mock file in the same folder for testing
    # TODO: change to real data
    mock_analized_image = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cars_test.png')

    img = cv2.imread(mock_analized_image)
    ret = dm.predict(img)

    parsed_result = DetectionModel.parse_result(ret)

    img_cpy = copy.deepcopy(img)
    MyAnnotator.draw_all_boxes(parsed_result, img_cpy)
    MyAnnotator.draw_all_names(parsed_result, img_cpy)

    mock_address_str = 'Москва, Ленина, д.1'
    mock_img_id = 'abc123efg'

    pathlib.Path(PARKING_IMGS_PATH).mkdir(exist_ok=True)

    path_to_save_img = os.path.join(PARKING_IMGS_PATH, mock_img_id + '.png')

    if not cv2.imwrite(path_to_save_img, img_cpy):
         raise Exception("Could not write image")

    return ParkingInfoResult(
        imgUrl=get_parking_image_url(mock_img_id),
        address=mock_address_str,
        allParkingPlaces=0,
        freeParkingPlaces=0
    )


@router.get(
    "/images/{image_id}",
    responses={
        200: {
            "content": {"image": {}}
        },
        404: {
            "content": {"description": "Not found"}
        }
    },
    response_class=Response,
    summary="Получить фото по id."
)
def get_image_by_id(image_id: str):
    path_to_image = os.path.join(PARKING_IMGS_PATH, image_id + '.png')
    img = cv2.imread(path_to_image)

    content = None

    try:
        content = cv2.imencode('.png', img)[1].tobytes()
    except:
        return Response(status_code=404, content=json.dumps({"description": "Not found"}), headers={"Content-Type": "application/json"})

    return StreamingResponse(io.BytesIO(content), media_type='image/png')


@router.get(
    "/user-images-2/",
    # responses={
    #     200: {
    #         "content": {"image": {}}
    #     }
    # },
    # response_class=Response,
    summary="Получить фото по id."
)
def get_image_by_id(
):
    imgPath = os.path.dirname(os.path.realpath(__file__)) + '/cars_test.png'
    img = cv2.imread(imgPath)
    ret = dm.predict(img)

    parsed_result = DetectionModel.parse_result(ret)
    img_cpy = copy.deepcopy(img)
    MyAnnotator.draw_all_boxes(parsed_result, img_cpy)
    MyAnnotator.draw_all_names(parsed_result, img_cpy)
    cv2.imwrite('annotated.png', img_cpy)

    content = cv2.imencode('.png', img_cpy)[1].tobytes()

    return StreamingResponse(io.BytesIO(content), media_type='image/jpeg')
    # return Response(encoded_img, media_type='image/jpeg')
