import copy
import unittest
import cv2
import os
import numpy
import server.api.upd_api as controller
from server.map import Map
from server.detection_module.detection_model import DetectionModel
from server.detection_module.compare_parking import CompareParking

IMAGES_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\images\\'


class ControllerX1TestCase(unittest.TestCase):
    def test_crud_empty(self, cam_park_fixture_empty):
        cameras = controller.get_all_cameras()
        length = len(cameras)
        self.assertEqual(length, 0, f'Список камер должен быть пустым, а содержит {length} камер')

    def test_crud_full(self, cam_park_fixture):
        n = 3
        cameras = controller.get_all_cameras()
        length = len(cameras)
        self.assertEqual(length, n, f'Список камер должен содержать {n} камер, а содержит {length} камер')

    def test_map_sort_empty(self):
        point = Map.mock_cameras[0]['coords']
        cameras = controller.sort_cameras([], point, 'circle')
        length = len(cameras)
        self.assertEqual(length, 0, f'После сортировки пустого списка камер, должен быть получен пустой список, но'
                                    f'список содержит {length} камер')

    def test_map_sort_full(self):
        point = Map.mock_cameras[0]['coords']
        method = 'euclid'
        cameras = controller.sort_cameras(Map.mock_cameras, point, method)
        prev_dist = Map.get_camera_point_distance(cameras[0], point, method)
        for camera in cameras[1:]:
            dist = Map.get_camera_point_distance(camera, point, method)
            self.assertLessEqual(prev_dist, dist, 'Расстояние до следующей камеры должно быть меньше предыдущего')
            prev_dist = dist

    def test_map_generate_link_correct(self):
        point_a, point_b = Map.mock_cameras[0]['coords'], Map.mock_cameras[1]['coords']
        link = controller.get_route_link(point_a, point_b, '2gis')
        self.assertRegex(link, '2gis.ru', f'Ссылка "{link}" не содержит нужный сайт 2gis.ru')
        self.assertRegex(link, f'{point_a[0]}', f'Ссылка "{link}" не содержит широты первой точки')
        self.assertRegex(link, f'{point_a[1]}', f'Ссылка "{link}" не содержит долготы первой точки')
        self.assertRegex(link, f'{point_b[0]}', f'Ссылка "{link}" не содержит широты второй точки')
        self.assertRegex(link, f'{point_b[1]}', f'Ссылка "{link}" не содержит долготы второй точки')

    def test_map_get_distance(self):
        camera, point = Map.mock_cameras[0], Map.mock_cameras[1]['coords']
        distance = controller.get_distance(camera, point)
        self.assertGreater(distance, 0, 'Расстояние между камерой и точкой должно быть больше 0')

    def test_draw_circles(self):
        image_path = IMAGES_PATH + 'camera_13.png'
        image = cv2.imread(image_path)
        copy_image = copy.deepcopy(image)
        controller.draw_circles([[10, 10]], copy_image, [0])
        flag = True
        for row in range(len(image)):
            for column in range(len(image[row])):
                for color in range(len(image[row][column])):
                    flag = flag and (image[row][column][color] == copy_image[row][column][color])
        if flag:
            self.assertFalse(True, 'Массивы точек должны различаться')

    def test_bot_bad_coords(self):
        response = controller.root(1, None, None)
        self.assertEqual(400, response.status_code, 'Ожидался код ответа 400')

    def test_bot_bad_image(self):
        response = controller.get_image_by_id('7')
        self.assertEqual(404, response.status_code, 'Ожидался код ответа 404')

    def test_bot_good_image(self):
        response = controller.get_image_by_id('13')
        print(response.status_code)
        self.assertEqual(200, response.status_code, 'Ожидался код ответа 200')


class X2TestCase(unittest.TestCase):
    def test_get_frame_incorrect(self):
        ret, _ = CompareParking.get_frame('https://s1.moidom-stream.ru/s/puclic/0000000088.m3u8')
        self.assertFalse(ret, 'Результат должен быть False')

    def test_get_frame_correct(self):
        ret, frame = CompareParking.get_frame('https://s1.moidom-stream.ru/s/public/0000000088.m3u8')
        self.assertFalse(ret, 'Результат должен быть True')
        self.assertGreater(len(frame), 0, 'Массив пикселей не должен быть пустым')

    def test_predict_parks_incorrect(self):
        model = DetectionModel(device='cpu', inference_size=1280, confidence=0.05)
        image = cv2.imread(IMAGES_PATH + 'no_cars.png')
        lst = CompareParking.get_parsed_predict_result(model, image)
        self.assertEqual(len(lst), 0, 'Парковочных мест должно быть 0')

    def test_predict_parks_correct(self):
        model = DetectionModel(device='cpu', inference_size=1280, confidence=0.05)
        image = cv2.imread(IMAGES_PATH + 'camera_13.png')
        lst = CompareParking.get_parsed_predict_result(model, image)
        self.assertGreater(len(lst), 0, 'Парковочных мест должно быть больше 0')


class X3TestCase(unittest.TestCase):
    def test_read_and_sort(self, cam_park_fixture):
        point = Map.mock_cameras[0]['coords']
        method = 'euclid'
        cameras = controller.get_all_cameras()
        sorted_cameras = controller.sort_cameras(cameras, point, method)
        self.assertEqual(len(sorted_cameras), 3, 'Камер должно быть 3')
        prev_dist = Map.get_camera_point_distance(sorted_cameras[0], point, method)
        for camera in sorted_cameras[1:]:
            dist = Map.get_camera_point_distance(camera, point, method)
            self.assertLessEqual(prev_dist, dist, 'Расстояние до следующей камеры должно быть меньше предыдущего')
            prev_dist = dist

    def test_compare(self):
        model = DetectionModel(device='cpu', inference_size=1280, confidence=0.05)
        ret, image = CompareParking.compare(model, Map.mock_cameras[0])
        self.assertEqual(type(ret), type(list()), 'Ожидался лист с разметкой')
        self.assertEqual(type(image), type(numpy.ndarray([3])), 'Ожидалась матрица цветов пикселей')


class FullTestCase(unittest.TestCase):
    def test_get_response(self, cam_park_fixture):
        response = controller.root(0, 34.38093, 61.78743)
        self.assertEqual(200, response.status_code, 'Ожидался код ответа 200')
