import unittest
from server import map

Map = map.Map()
Map.init()


class GenerateLinkTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.point_a = (61.81034, 34.32836)
        cls.point_b = (61.76542, 34.3142)

    def test_correct_sites(self):
        link = Map.generate_route_link(self.point_a, self.point_b, 'yandex')
        self.assertRegex(link, 'yandex.ru', 'При site="yandex" ссылка должна вести на сайт yandex.ru')

        link = Map.generate_route_link(self.point_a, self.point_b, '2gis')
        self.assertRegex(link, '2gis.ru', 'При site="2gis" Ссылка должна вести на сайт 2gis.ru')

    def test_incorrect_site(self):
        with self.assertRaises(ValueError):
            Map.generate_route_link(self.point_a, self.point_b, 'my_site')

    def test_correct_points(self):
        link = Map.generate_route_link(self.point_a, self.point_b)
        self.assertRegex(link, str(self.point_a[0]), 'При двух точках ссылка должна содержать широту первой точки')
        self.assertRegex(link, str(self.point_a[1]), 'При двух точках ссылка должна содержать долготу первой точки')
        self.assertRegex(link, str(self.point_b[0]), 'При двух точках ссылка должна содержать широту второй точки')
        self.assertRegex(link, str(self.point_b[1]), 'При двух точках ссылка должна содержать долготу второй точки')

        link = Map.generate_route_link(None, self.point_b)
        self.assertNotRegex(link, str(self.point_a[0]), 'При отсутствии первой точки ссылка не должна содержать '
                                                        'широту первой точки')
        self.assertNotRegex(link, str(self.point_a[1]), 'При отсутствии первой точки ссылка не должна содержать '
                                                        'долготу первой точки')
        self.assertRegex(link, str(self.point_b[0]), 'При отсутствии первой точки ссылка должна содержать '
                                                     'широту второй точки')
        self.assertRegex(link, str(self.point_b[1]), 'При отсутствии первой точки ссылка должна содержать '
                                                     'долготу второй точки')

    def test_correct_map_center(self):
        link = Map.generate_route_link(self.point_a, self.point_b)
        lat, lng = (self.point_a[0] + self.point_b[0]) / 2, (self.point_a[1] + self.point_b[1]) / 2
        self.assertRegex(link, str(lat), 'При двух точках широтой центра карты должна быть широта середины отрезка')
        self.assertRegex(link, str(lng), 'При двух точках долготой центра карты должна быть долгота середины отрезка')

        link = Map.generate_route_link(None, self.point_b)
        self.assertRegex(link, str(self.point_b[0]), 'При отсутствии первой точки широтой центра карты должна быть '
                                                     'широта второй точки')
        self.assertRegex(link, str(self.point_b[1]), 'При отсутствии первой точки долготой центра карты должна быть '
                                                     'долгота второй точки')


class DistanceTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.point_a = point_a = [61.81034, 34.32836]
        cls.point_b = [61.80943, 34.33114]
        cls.camera = {'camera_id': 2, 'camera_url': 'https://s1.moidom-stream.ru/s/public/0000000088.m3u8',
                      'coords': point_a, 'parking_places': []}

    def test_correct_methods(self):
        methods = [
            ['euclid', 'Расстояние находится неправильно методом Евклида'],
            ['circle', 'Сферическое расстояние находится неправильно'],
            ['dijkstra', 'Расстояние находится неправильно методом Дийкстры']
        ]

        for method, error_message in methods:
            distance_1 = Map.get_camera_point_distance(self.camera, self.point_b, method)
            distance_2 = Map.get_point_point_distance(self.camera['coords'], self.point_b, method)
            self.assertEqual(distance_1, distance_2, error_message)

    def test_incorrect_method(self):
        with self.assertRaises(ValueError):
            Map.get_camera_point_distance(self.camera, self.point_b, 'unknown_method')
        with self.assertRaises(ValueError):
            Map.get_point_point_distance(self.camera['coords'], self.point_b, 'unknown_method')


class SortTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.point = (61.81034, 34.32836)
        cls.cameras = Map.mock_cameras.copy()

    def test_correct_sort(self):
        methods = [
            ['euclid', 'Расстояние до следующей камеры должно быть >= чем расстояние до '
                       'текущей камеры при методе Евклида'],
            ['circle', 'Расстояние до следующей камеры должно быть >= чем расстояние до '
                       'текущей камеры при сферическом методе'],
            ['dijkstra', 'Расстояние до следующей камеры должно быть >= чем расстояние до '
                         'текущей камеры при методе Дийкстры']
        ]

        for method, error_message in methods:
            sorted_cameras = Map.sort_cameras(self.cameras, self.point, method)
            prev_dist = Map.get_camera_point_distance(sorted_cameras[0], self.point, method)
            for camera in sorted_cameras[1:]:
                dist = Map.get_camera_point_distance(camera, self.point, method)
                self.assertLessEqual(prev_dist, dist, error_message)
                prev_dist = dist

    def test_incorrect_sort(self):
        with self.assertRaises(ValueError):
            Map.sort_cameras(self.cameras, self.point, 'unknown_method')


if __name__ == '__main__':
    unittest.main()
