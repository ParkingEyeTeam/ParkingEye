import time
from typing import Union
from http.client import responses
import json
from math import dist
import cv2
from matplotlib.style import use
from pydantic import BaseModel
from typing import List, Optional
import torch
import os
import pathlib
import copy
from server import crud
from server.detection_module import DetectionModel
from server.detection_module.drawing import MyAnnotator
import gc
import io
from starlette.responses import StreamingResponse
from server.detection_module import compare_parking
from server.map import Map

from fastapi import Response, APIRouter

from server.schemas.cam_park import CameraParking

gc.collect()
torch.cuda.empty_cache()
dm = DetectionModel(device='cpu')

router = APIRouter()

Map.init()

camera_parking_repository = crud.camera_parking

PARKING_IMGS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'parking_imgs')


def get_parking_image_url(image_id):
    apiUrl = 'http://localhost:8000/images/'
    return apiUrl + str(image_id)


class ParkingInfoResult(BaseModel):
    imgUrl: str
    address: str
    allParkingPlaces: int
    freeParkingPlaces: int
    mapServiceLink2GIS: str
    mapServiceLinkYandex: str
    distance: int
    cameraId: int
    prevCameraId: Union[int, None]
    coords: List[float]


def write_image_and_create_result(camera: CameraParking, places_info, img, user_coords, prev_camera_id):
    free_places = sum(i == 0 for i in places_info)
    all_places = sum(i >= 0 for i in places_info)

    img_cpy = copy.deepcopy(img)

    MyAnnotator.put_all_circle(camera['parking_places'], img_cpy, places_info)

    int_camera_id = int(camera['camera_id'])

    path_to_save_img = os.path.join(PARKING_IMGS_PATH, str(int_camera_id) + '.png')
    if not os.path.exists(PARKING_IMGS_PATH):
        os.mkdir(PARKING_IMGS_PATH)
    if not cv2.imwrite(path_to_save_img, img_cpy):
        raise Exception("Could not write image")

    return ParkingInfoResult(
        address=camera['address'],
        freeParkingPlaces=free_places,
        allParkingPlaces=all_places,
        imgUrl=get_parking_image_url(int_camera_id),
        mapServiceLink2GIS=Map.generate_route_link(user_coords, (camera['coords'][0], camera['coords'][1]), '2gis'),
        mapServiceLinkYandex=Map.generate_route_link(user_coords, (camera['coords'][0], camera['coords'][1]), 'yandex'),
        distance=int(Map.get_camera_point_distance(camera, user_coords)),
        cameraId=int(camera['camera_id']),
        coords=list(user_coords),
        prevCameraId=prev_camera_id
    )


def get_available_cameras(sorted_cameras, last_camera_id):
    if last_camera_id is None: return sorted_cameras

    can_use_camera = False

    cameras_to_process = []

    for camera in sorted_cameras:
        if can_use_camera:
            cameras_to_process.append(camera)

        if int(camera['camera_id']) == last_camera_id:
            can_use_camera = True

    return cameras_to_process


# Use http://localhost:8000/?longitude=34.354423&latitude=61.787439 for example

@router.get(
    "/",
    responses={
        400: {"description": "longitude and latitude are required"},
        404: {"description": "No free parking places found"},
    },
    response_model=ParkingInfoResult
)
def root(last_camera_id: Optional[int] = None, longitude: float = None, latitude: float = None):
    if longitude is None or latitude is None:
        return Response(
            status_code=400,
            content=json.dumps({"desription": "longitude and latitude are required"}),
            media_type="application/json",
        )
    startTime = time.time()

    all_cameras = camera_parking_repository.read_all()

    endTime = time.time()

    print("Read all cameras: " + str(endTime - startTime))

    user_coords = (latitude, longitude)

    startTime = time.time()

    sorted_cameras = Map.sort_cameras(all_cameras, user_coords, method='euclid')

    endTime = time.time()

    print("Sort cameras: " + str(endTime - startTime))

    startTime = time.time()

    for camera in get_available_cameras(sorted_cameras, last_camera_id):
        pass
    print("Get available cameras: " + str(endTime - startTime))

    for camera in get_available_cameras(sorted_cameras, last_camera_id):

        places_info, img = compare_parking.CompareParking.compare(dm, camera)
        has_free_places = any(i == 0 for i in places_info)

        if has_free_places:
            print("Found free parking places: " + str(time.time() - startTime))
            return write_image_and_create_result(camera, places_info, img, user_coords, last_camera_id)

    return Response(
        status_code=404,
        content=json.dumps({"description": "No free parking places found"}),
        media_type="application/json",
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
        return Response(status_code=404, content=json.dumps({"description": "Not found"}),
                        headers={"Content-Type": "application/json"})

    return StreamingResponse(io.BytesIO(content), media_type='image/png')
