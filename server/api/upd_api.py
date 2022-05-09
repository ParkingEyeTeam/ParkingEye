from typing import Union
import json
import cv2
from pydantic import BaseModel
from typing import List, Optional
import torch
import os
import copy
from server import crud
from server.detection_module import DetectionModel
from server.detection_module.drawing import MyAnnotator
import gc
import io
from starlette.responses import StreamingResponse
from server.detection_module.compare_parking import CompareParking
from server.map import Map
from fastapi import Response, APIRouter

PARKING_IMAGES_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'parking_imgs')
MAP_METHOD = 'circle'

gc.collect()
torch.cuda.empty_cache()
dm = DetectionModel(device='cpu', inference_size=1280, confidence=0.05)
router = APIRouter()
Map.init()


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


def get_parking_image_url(image_id):
    api_url = 'http://localhost:8000/images/'
    return f'{api_url}{image_id}'


def get_all_cameras():
    return crud.camera_parking.read_all()


def sort_cameras(cameras, point, method=MAP_METHOD):
    return Map.sort_cameras(cameras, point, method)


def get_available_cameras(sorted_cameras, last_camera_id):
    if last_camera_id is None:
        return sorted_cameras

    length = len(sorted_cameras)
    if last_camera_id == int(sorted_cameras[length-1]['camera_id']):
        return []

    for i in range(length):
        if int(sorted_cameras[i]['camera_id']) == last_camera_id:
            return sorted_cameras[i+1:]

    return sorted_cameras


def get_route_link(point_a, point_b, site):
    return Map.generate_route_link(point_a, point_b, site)


def get_distance(camera, point, method=MAP_METHOD):
    return int(Map.get_camera_point_distance(camera, point, method))


def draw_circles(parking_places, image, places_info):
    MyAnnotator.put_all_circle(parking_places, image, places_info)


def write_image_and_create_result(camera, places_info, img, user_coords, prev_camera_id):
    free_places = sum(i == 0 for i in places_info)
    all_places = sum(i >= 0 for i in places_info)

    img_cpy = copy.deepcopy(img)
    draw_circles(camera['parking_places'], img_cpy, places_info)

    int_camera_id = int(camera['camera_id'])

    path_to_save_img = os.path.join(PARKING_IMAGES_PATH, str(int_camera_id) + '.png')
    if not os.path.exists(PARKING_IMAGES_PATH):
        os.mkdir(PARKING_IMAGES_PATH)
    if not cv2.imwrite(path_to_save_img, img_cpy):
        raise Exception("Could not write image")

    return ParkingInfoResult(
        address=camera['address'],
        freeParkingPlaces=free_places,
        allParkingPlaces=all_places,
        imgUrl=get_parking_image_url(int_camera_id),
        mapServiceLink2GIS=get_route_link(user_coords, (camera['coords'][0], camera['coords'][1]), '2gis'),
        mapServiceLinkYandex=get_route_link(user_coords, (camera['coords'][0], camera['coords'][1]), 'yandex'),
        distance=get_distance(camera, user_coords),
        cameraId=int(camera['camera_id']),
        coords=list(user_coords),
        prevCameraId=prev_camera_id
    )


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
            content=json.dumps({"description": "longitude and latitude are required"}),
            media_type="application/json",
        )

    all_cameras = get_all_cameras()

    user_coords = (latitude, longitude)
    sorted_cameras = sort_cameras(all_cameras, user_coords)

    for camera in get_available_cameras(sorted_cameras, last_camera_id):
        places_info, img = CompareParking.compare(dm, camera)
        has_free_places = any(i == 0 for i in places_info)

        if has_free_places:
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
    path_to_image = os.path.join(PARKING_IMAGES_PATH, image_id + '.png')
    img = cv2.imread(path_to_image)

    try:
        content = cv2.imencode('.png', img)[1].tobytes()
    except:
        return Response(status_code=404, content=json.dumps({"description": "Not found"}),
                        headers={"Content-Type": "application/json"})

    return StreamingResponse(io.BytesIO(content), media_type='image/png')
