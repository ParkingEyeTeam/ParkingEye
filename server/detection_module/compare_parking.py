import copy
import time

import cv2
import numpy as np

from server.schemas.cam_park import CameraParking
from server.detection_module import DetectionModel


def is_included(bbox, point, pad=20):
    if bbox[0] - pad <= point[0] <= bbox[2] + pad and bbox[1] - pad <= point[1] <= bbox[3] + pad:
        return True
    return False


class CompareParking:
    @staticmethod
    def compare(model: DetectionModel, camera_parking):
        """
        Выкидвывает ошибку ConnectionError, если не получилось взять кадр
        1, если i-я парковка в Camera_Parking.parking_places занята
        0, если i-й парковка в Camera_Parking.parking_places свободна
        """
        ret, image = CompareParking.get_frame(camera_parking['camera_url'])

        if not ret:
            raise ConnectionError

        preds = model.predict(image)
        parsed_res = DetectionModel.parse_result(preds)

        ret = CompareParking.compare_places_with_bboxes(parsed_res, camera_parking)
        return ret, image

    @staticmethod
    def compare_places_with_bboxes(parsed_res, camera_parking):
        ret = []
        for i in range(len(camera_parking['parking_places'])):
            f = 0
            for j in range(len(parsed_res)):
                if is_included(parsed_res[j].bbox, camera_parking['parking_places'][i]):
                    f = 1
                    break
            ret.append(f)
        return ret

    @staticmethod
    def get_frame(camera_url: str):
        cap = cv2.VideoCapture(camera_url)
        ret, frame = cap.read()
        cap.release()
        return ret, frame
