import cv2
import numpy as np

from server.detection_module.detection_model import ParsedResult
from typing import List


class MyAnnotator:
    @staticmethod
    def put_text(frame, text, position, scale=1, color=(0, 0, 255), thickness=2):
        """
        Добавляет текст на изображение
        """
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_COMPLEX, scale, color, thickness)

    @staticmethod
    def rectangle(frame, start, end, color=(0, 0, 255), thickness=2):
        """
        Рисует квадрат на изображении
        """
        cv2.rectangle(frame, start, end, color, thickness)

    @staticmethod
    def draw_all_boxes(results: List[ParsedResult], img: np.ndarray,
                       classes: List[str] = ('car', 'track')):
        """
        Отрисовывает боксы на картинке.
        """
        for res in results:
            start = (res.bbox[0], res.bbox[1])
            end = (res.bbox[2], res.bbox[3])
            if res.category_name in classes:
                MyAnnotator.rectangle(img, start, end)

    @staticmethod
    def draw_all_names(results: List[ParsedResult], img: np.ndarray,
                       classes: List[str] = ('car', 'track')):
        """
        Отрисовывает надписи на картинке.
        """
        for res in results:
            start = (res.bbox[0] + 20, res.bbox[1])
            # end = (res.bbox[2], res.bbox[3])
            if res.category_name in classes:
                MyAnnotator.put_text(img, res.category_name, start)

    @staticmethod
    def put_circle(point, frame, empty=1):
        if empty == 1:
            cv2.circle(frame, point, 5, (0, 255, 0), -1)
        else:
            cv2.circle(frame, point, 5, (0, 0, 255), -1)

    @staticmethod
    def put_all_circle(parking_places, frame, empty: list):
        for point, empty_i in zip(parking_places, empty):
            MyAnnotator.put_circle(point, frame, empty_i)
