import unittest
import server.api.upd_api as controller
from server.map import Map


class ControllerX1TestCase(unittest.TestCase):
    def test_crud_empty(self):
        # Сделать БД пустой
        cameras = controller.get_all_cameras()
        length = len(cameras)
        self.assertEqual(length, 0, f'Список камер должен быть пустым, а содержит {length} камер')

    def test_crud_full(self):
        # Заполнить БД n камерами
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

    def test_map_get_distance(self):
        camera, point = Map.mock_cameras[0], Map.mock_cameras[1]['coords']
        distance = controller.get_distance(camera, point)
        self.assertGreater(distance, 0, 'Расстояние между камерой и точкой должно быть больше 0')
