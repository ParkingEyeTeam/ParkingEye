import pytest
from pymongo import MongoClient
from server import schemas
from server.crud import mongo_config

"""
Сециальный файл pytest для фикстур.
Чтобы использовать фикстуру в тесте, нужно передать имя
метода фикстуры в качестве аргумента.
"""


@pytest.fixture()
def cam_park_fixture():
    """Подключение к БД и ее заполнение тестовыми данными перед тестами"""
    connection = MongoClient(mongo_config.mongo_connection_string)
    db = connection.get_database("test_server_db")
    db.drop_collection("camera_parking")
    items = [
        schemas.CameraParking(
            camera_id=1,
            camera_url="https://s1.moidom-stream.ru/camera1",
            coords=[61, 34],
            parking_places=[[329, 179], [308, 193], [924, 374]]
        ),
        schemas.CameraParking(
            camera_id=2,
            camera_url="https://s1.moidom-stream.ru/camera2",
            coords=[24, 67],
            parking_places=[[123, 563], [238, 444]]
        ),
        schemas.CameraParking(
            camera_id=3,
            camera_url="https://s1.moidom-stream.ru/camera3",
            coords=[78, 11],
            parking_places=[[463, 543], [568, 224], [183, 426], [134, 429]]
        ),
    ]
    for item in items:
        db.camera_parking.insert_one(dict(item))
    connection.close()
