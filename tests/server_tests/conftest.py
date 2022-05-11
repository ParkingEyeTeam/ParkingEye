import pytest
from pymongo import MongoClient
from server import schemas
from server.crud import mongo_config

"""
Специальный файл pytest для фикстур.
Чтобы использовать фикстуру в тесте, нужно передать имя
метода фикстуры в качестве аргумента.
"""


def cam_park():
    """Подключение к БД и ее заполнение тестовыми данными перед тестами"""
    connection = MongoClient(mongo_config.mongo_connection_string)
    db = connection.get_database("test_server_db")
    db.drop_collection("camera_parking")
    items = [
        schemas.CameraParking(
            camera_id=1,
            camera_url="https://s1.moidom-stream.ru/camera1",
            coords=[61, 34],
            parking_places=[[329, 179], [308, 193], [924, 374]],
            address="Проспект Карла Маркса, 19"
        ),
        schemas.CameraParking(
            camera_id=2,
            camera_url="https://s1.moidom-stream.ru/camera2",
            coords=[24, 67],
            parking_places=[[123, 563], [238, 444]],
            address="Проспект Карла Маркса, 19"
        ),
        schemas.CameraParking(
            camera_id=3,
            camera_url="https://s1.moidom-stream.ru/camera3",
            coords=[78, 11],
            parking_places=[[463, 543], [568, 224], [183, 426], [134, 429]],
            address="Проспект Карла Маркса, 19"
        ),
    ]
    for item in items:
        db.camera_parking.insert_one(dict(item))
    connection.close()


def cam_park_for_api():
    """Подключение к БД и ее заполнение тестовыми данными перед тестами"""
    connection = MongoClient(mongo_config.mongo_connection_string)
    db = connection.get_database("test_server_db")
    db.drop_collection("camera_parking")
    items = [
        {
            "camera_id": 20,
            "camera_url": "https://s1.moidom-stream.ru/s/public/0000000088.m3u8",
            "address": "Проспект Карла Маркса, 19",
            "coords": [61.78749, 34.38096],
            "parking_places": [[925, 375], [880, 380], [487, 383], [531, 382], [634, 382],
                               [354, 388], [259, 390], [305, 391], [400, 390]]
        },
        {
            "camera_id": 6,
            "camera_url": "https://s1.moidom-stream.ru/s/public/0000006567.m3u8",
            "address": "Краснофлотская, 20",
            "coords": [61.8022, 34.32632],
            "parking_places": [[1851, 338], [1491, 391], [436, 429], [308, 458], [1806, 469],
                               [146, 485], [1714, 497], [1647, 503], [1585, 512]]
        },
        {
            "camera_id": 5,
            "camera_url": "https://s1.moidom-stream.ru/s/public/0000001415.m3u8",
            "address": "Набережная Варкауса, 21",
            "coords": [61.80657, 34.3396],
            "parking_places": [[790, 364], [781, 398], [749, 419], [672, 508], [645, 541],
                               [611, 569], [572, 596], [542, 633], [508, 670], [471, 694]]
        },
    ]
    for item in items:
        db.camera_parking.insert_one(dict(item))
    connection.close()


def cam_park_empty():
    connection = MongoClient(mongo_config.mongo_connection_string)
    db = connection.get_database("test_server_db")
    db.drop_collection("camera_parking")
    connection.close()


@pytest.fixture()
def cam_park_fixture():
    cam_park()


@pytest.fixture()
def cam_park_fixture_empty():
    cam_park_empty()


@pytest.fixture()
def cam_park_fixture_for_api():
    cam_park_for_api()


@pytest.fixture()
def park_fixture():
    """Подключение к БД и ее заполнение тестовыми данными перед тестами"""
    connection = MongoClient(mongo_config.mongo_connection_string)
    db = connection.get_database("test_server_db")
    db.drop_collection("parking")
    items = [
        schemas.Parking(
            camera_id=20,
            timestamp=20140812007401,
            image="server/tests/server_tests/images/image20.png",
            empty_places=[[925, 375], [880, 380], [487, 383]],
            taken_places=[[531, 382], [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]],
        ),
        schemas.Parking(
            camera_id=6,
            timestamp=3213213213321,
            image="server/tests/server_tests/images/image20.png",
            empty_places=[[925, 375], [880, 380], [487, 383]],
            taken_places=[[531, 382], [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]],
        ),
        schemas.Parking(
            camera_id=8,
            timestamp=20140321327401,
            image="server/tests/server_tests/images/image20.png",
            empty_places=[[925, 375], [880, 380], [487, 383]],
            taken_places=[[531, 382], [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]],
        ),
    ]
    for item in items:
        db.parking.insert_one(dict(item))
    connection.close()
