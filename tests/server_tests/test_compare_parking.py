import unittest
from server.detection_module.compare_parking import CompareParking, FramesReader
import numpy as np
import cv2
import time
import os
import pytest
from server.detection_module.detection_model import ParsedResult


# class CompareParkingTest(unittest.TestCase):
@pytest.mark.parametrize('camera_url, address',
                         [('https://s1.moidom-stream.ru/s/public/0000000088.m3u8', 'Проспект Карла Маркса, 19'),
                          ('https://s1.moidom-stream.ru/s/public/0000006567.m3u8', 'Краснофлотская, 20'),
                          ('https://s1.moidom-stream.ru/s/public/0000001415.m3u8', 'Набережная Варкауса, 21'),
                          ])
def test_get_frame_ok(camera_url, address):
    ret, frame = FramesReader.get_frame(camera_url)
    assert ret is not None, f'Камера на {address} недоступна'


def test_get_frame_bad():
    ret, frame = FramesReader.get_frame('https://s1.moidom-stream.ru/s/public/random_number.m3u8')
    assert ret is False, f'Неверный флага возврата неудачи'


@pytest.mark.parametrize('places, empties',
                         [
                             ({'parking_places': [[100, 200], [310, 410]]}, [1, 1]),
                             ({'parking_places': [[1000, 1000], [310, 610]]}, [0, 1]),
                             ({'parking_places': [[100, 200], [1000, 1000], [310, 410]]}, [1, 0, 1]),
                             ({'parking_places': []}, []),
                         ]
                         )
def test_compare_places_with_bboxes(places, empties):
    parsed_res = [ParsedResult(bbox=[100, 200, 300, 400], confidence=1, category_id=2, category_name='car'),
                  ParsedResult(bbox=[300, 600, 400, 700], confidence=1, category_id=2, category_name='car'),
                  ParsedResult(bbox=[100, 200, 800, 800], confidence=1, category_id=2, category_name='car'),
                  ]
    ret = CompareParking.compare_places_with_bboxes(parsed_res, places)
    assert ret == empties, "not equal"


def test_time_to_get_frame():
    t = time.time()
    ret, frame = FramesReader.get_frame('https://s1.moidom-stream.ru/s/public/0000000088.m3u8')
    max_time = 0.5
    assert time.time() - t <= max_time, f'Время на получение кадра > {max_time} секунд'
