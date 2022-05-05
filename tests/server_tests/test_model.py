import unittest
from server.detection_module.detection_model import DetectionModel
import cv2
import time
import os


class DetectionModelTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = DetectionModel(device='cpu', inference_size=1280, confidence=0.05)

    def test_inference_time(self):
        img = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/test_img_2.jpg')
        t = time.time()
        _ = self.model.predict(img)
        max_inf = 2

        self.assertLessEqual(time.time() - t, max_inf, f'Время инференса > {max_inf} секунд')

    def test_cars_amount_detect(self):
        img = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/test_img_2.jpg')
        pred = self.model.predict(img)
        parsed = DetectionModel.parse_result(pred)

        self.assertEqual(3, len(parsed), 'Неверное число автомобилей на картинке')

    def test_cars_amount_from_camera(self):
        img = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/test_camera_cars.jpg')
        pred = self.model.predict(img)
        parsed = DetectionModel.parse_result(pred)

        self.assertEqual(3, len(parsed), 'Неверное число автомобилей на картинке')

    def test_cars_amount_no_cars(self):
        img = cv2.imread(os.path.dirname(os.path.realpath(__file__)) + '/no_cars.jpeg')
        pred = self.model.predict(img)
        parsed = DetectionModel.parse_result(pred)

        self.assertEqual(0, len(parsed), 'Неверное число автомобилей на картинке')
