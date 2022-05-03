import unittest
import math
from server import map


class GenerateLinkTestCase(unittest.TestCase):
    def setUp(self):
        self.point_a = (61.81034, 34.32836)
        self.point_b = (61.76542, 34.3142)
        self.map = map.Map()
        self.map.init()

    def test_correct_sites(self):
        link = self.map.generate_route_link(self.point_a, self.point_b, 'yandex')
        self.assertRegex(link, 'yandex.ru', 'При site="yandex" ссылка должна вести на сайт yandex.ru')

        link = self.map.generate_route_link(self.point_a, self.point_b, '2gis')
        self.assertRegex(link, '2gis.ru', 'При site="2gis" Ссылка должна вести на сайт 2gis.ru')

        with self.assertRaises(ValueError):
            self.map.generate_route_link(self.point_a, self.point_b, 'my_site')

    def test_correct_points(self):
        link = self.map.generate_route_link(self.point_a, self.point_b)
        self.assertRegex(link, str(self.point_a[0]), 'При двух точках ссылка должна содержать широту первой точки')
        self.assertRegex(link, str(self.point_a[1]), 'При двух точках ссылка должна содержать долготу первой точки')
        self.assertRegex(link, str(self.point_b[0]), 'При двух точках ссылка должна содержать широту второй точки')
        self.assertRegex(link, str(self.point_b[1]), 'При двух точках ссылка должна содержать долготу второй точки')

        link = self.map.generate_route_link(None, self.point_b)
        self.assertNotRegex(link, str(self.point_a[0]), 'При отсутствии первой точки ссылка не должна содержать '
                                                        'широту первой точки')
        self.assertNotRegex(link, str(self.point_a[1]), 'При отсутствии первой точки ссылка не должна содержать '
                                                        'долготу первой точки')
        self.assertRegex(link, str(self.point_b[0]), 'При отсутствии первой точки ссылка должна содержать '
                                                     'широту второй точки')
        self.assertRegex(link, str(self.point_b[1]), 'При отсутствии первой точки ссылка должна содержать '
                                                     'долготу второй точки')

    def test_correct_map_center(self):
        link = self.map.generate_route_link(self.point_a, self.point_b)
        lat, lng = (self.point_a[0] + self.point_b[0]) / 2, (self.point_a[1] + self.point_b[1]) / 2
        self.assertRegex(link, str(lat), 'При двух точках широтой центра карты должна быть широта середины отрезка')
        self.assertRegex(link, str(lng), 'При двух точках долготой центра карты должна быть долгота середины отрезка')

        link = self.map.generate_route_link(None, self.point_b)
        self.assertRegex(link, str(self.point_b[0]), 'При отсутствии первой точки широтой центра карты должна быть '
                                                     'широта второй точки')
        self.assertRegex(link, str(self.point_b[1]), 'При отсутствии первой точки долготой центра карты должна быть '
                                                     'долгота второй точки')

    def tearDown(self):
        pass


class DistanceTestCase(unittest.TestCase):
    def setUp(self):
        self.point_a = [61.81034, 34.32836]
        self.point_b = [61.80943, 34.33114]
        self.camera = {'camera_id': 2, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
                       'coords': self.point_a, 'parking_places': []}
        self.map = map.Map()
        self.map.init()

    def test_correct_methods(self):
        distance_1 = self.map.get_camera_point_distance(self.camera, self.point_b, 'dijkstra')
        distance_2 = self.map.get_point_point_distance(self.camera['coords'], self.point_b, 'dijkstra')
        self.assertEqual(distance_1, distance_2, 'Расстояние находится неправильно методом Дийкстры')

        distance_1 = self.map.get_camera_point_distance(self.camera, self.point_b, 'euclid')
        distance_2 = self.map.get_point_point_distance(self.camera['coords'], self.point_b, 'euclid')
        lat_dif, lng_dif = self.point_a[0] - self.point_b[0], self.point_a[1] - self.point_b[1]
        distance_3 = math.sqrt(lat_dif * lat_dif + lng_dif * lng_dif)
        self.assertEqual(distance_1, distance_2, 'Расстояние находится неправильно методом Евклида')
        self.assertEqual(distance_1, distance_3, 'Расстояние находится неправильно методом Евклида')

        with self.assertRaises(ValueError):
            self.map.get_camera_point_distance(self.camera, self.point_b, 'unknown_method')
        with self.assertRaises(ValueError):
            self.map.get_point_point_distance(self.camera['coords'], self.point_b, 'unknown_method')

    def tearDown(self):
        pass


class SortTestCase(unittest.TestCase):
    def setUp(self):
        self.point = (61.81034, 34.32836)
        self.map = map.Map()
        self.cameras = self.map.mock_cameras.copy()
        self.map.init()

    def test_correct_sort(self):
        method = 'dijkstra'
        sorted_cameras = self.map.sort_cameras(self.cameras, self.point, method)
        prev_dist = self.map.get_camera_point_distance(sorted_cameras[0], self.point, method)
        for camera in sorted_cameras[1:]:
            dist = self.map.get_camera_point_distance(camera, self.point, method)
            self.assertLessEqual(prev_dist, dist, 'Расстояние до следующей камеры должно быть >= чем расстояние до '
                                                  'текущей камеры при методе Дийкстры')
            prev_dist = dist

        method = 'euclid'
        sorted_cameras = self.map.sort_cameras(self.cameras, self.point, method)
        prev_dist = self.map.get_camera_point_distance(sorted_cameras[0], self.point, method)
        for camera in sorted_cameras[1:]:
            dist = self.map.get_camera_point_distance(camera, self.point, method)
            self.assertLessEqual(prev_dist, dist, 'Расстояние до следующей камеры должно быть >= чем расстояние до '
                                                  'текущей камеры при методе Евклида')
            prev_dist = dist

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
