from fastapi.testclient import TestClient
from server import crud
from server.api.upd_api import get_parking_image_url, router

"""
Пример тестирования FastAPI.
Тесты и эндпоинты могут находиться в разных файлах,
необходимо только импортировать app в файл теста.
"""

crud.camera_parking = crud.cam_park.CRUDCameraParking("test_server_db")

client = TestClient(router)


def test_get_parking_info_without_query_params():
    response = client.get('/')
    assert response.status_code == 400, 'Неверный код ответа'
    assert response.json() == {"description": "longitude and latitude are required"}, 'Неверное тело ответа'


def test_get_parking_info_with_only_longitude():
    response = client.get('/?longitude=1')
    assert response.status_code == 400, 'Неверный код ответа'
    assert response.json() == {"description": "longitude and latitude are required"}, 'Неверное тело ответа'


def test_get_parking_info_with_only_latitude():
    response = client.get('/?latitude=1')
    assert response.status_code == 400, 'Неверный код ответа'
    assert response.json() == {"description": "longitude and latitude are required"}, 'Неверное тело ответа'


def test_get_parking_info_with_correct_geoposition(cam_park_fixture_for_api):
    response = client.get('/?latitude=61.78749&longitude=34.38096')
    assert response.status_code == 200, 'Неверный код ответа'
    response_json = response.json()
    assert response_json['address'] == 'Проспект Карла Маркса, 19', 'Неверно определён адрес'
    assert response_json['cameraId'] == 20, 'Неверно определена камера'
    assert response_json['prevCameraId'] is None, 'Неверно определена предыдущая камера'
    assert response_json['imgUrl'] == get_parking_image_url(20), 'Неверно сформирован url картинки'


def test_get_parking_info_with_correct_geoposition_and_last_camera_id(cam_park_fixture_for_api):
    response = client.get('/?latitude=61.78749&longitude=34.38096&last_camera_id=20')
    assert response.status_code == 200, 'Неверный код ответа'
    response_json = response.json()
    assert response_json['address'] != 'Проспект Карла Маркса, 19', 'Неверно определён адрес'
    assert response_json['cameraId'] != 20, 'Неверно определена камера'
    assert response_json['prevCameraId'] == 20, 'Неверно определена предыдущая камера'
    assert response_json['imgUrl'] != get_parking_image_url(20), 'Неверно сформирован url картинки'


def test_get_parking_info_when_has_no_parking_places(cam_park_fixture_empty):
    response = client.get('/?latitude=61.78749&longitude=34.38096')
    assert response.status_code == 404, 'Неверный код ответа'
    assert response.json() == {"description": "No free parking places found"}, 'Неверное тело ответа'
