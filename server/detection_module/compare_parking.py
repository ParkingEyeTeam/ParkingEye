import copy
import time

import cv2
import numpy as np

from server.schemas.cam_park import CameraParking
from server.detection_module import DetectionModel


def is_included(bbox, point):
    if bbox[0] < point[0] < bbox[2] and bbox[1] < point[1] < bbox[3]:
        return True
    return False


class CompareParking:
    @staticmethod
    def compare(model: DetectionModel, image: np.ndarray, camera_parking: CameraParking):
        """
        1, если i-й элемент занят
        0, если i-й элемент свободен
        """
        preds = model.predict(image)
        parsed_res = DetectionModel.parse_result(preds)
        ret = []
        for i in range(len(camera_parking.parking_places)):
            f = 0
            for j in range(len(parsed_res)):
                if is_included(parsed_res[j].bbox, camera_parking.parking_places[i]):
                    f = 1
                    break
            ret.append(f)
        return ret
