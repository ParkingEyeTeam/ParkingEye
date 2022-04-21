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
    def compare(model: DetectionModel, camera_parking: CameraParking):
        """
        Выкидвывает ошибку ConnectionError, если не получилось взять кадр
        1, если i-я парковка в Camera_Parking.parking_places занята
        0, если i-й парковка в Camera_Parking.parking_places свободна
        """
        startTime = time.time()
        ret, image = CompareParking.get_frame(camera_parking['camera_url'])
        print('get_frame:', time.time() - startTime)

        if not ret:
            raise ConnectionError
        startTime = time.time()

        preds = model.predict(image)
        parsed_res = DetectionModel.parse_result(preds)

        print('predict:', time.time() - startTime)

        startTime = time.time()
        ret = []
        for i in range(len(camera_parking['parking_places'])):
            f = 0
            for j in range(len(parsed_res)):
                if is_included(parsed_res[j].bbox, camera_parking['parking_places'][i]):
                    f = 1
                    break
            ret.append(f)

        print('parse_result:', time.time() - startTime)
        return ret, image

    @staticmethod
    def get_frame(camera_url: str):
        cap = cv2.VideoCapture(camera_url)
        ret, frame = cap.read()
        cap.release()
        return ret, frame
