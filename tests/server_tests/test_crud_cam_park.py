from server import crud, schemas


def test_read_all(cam_park_fixture):
    camera_parking = crud.cam_park.CRUDCameraParking("test_server_db")
    response_list = camera_parking.read_all()
    assert len(response_list) == 3, "Количество элементов не соответствует ожидаемому числу!"


def test_read(cam_park_fixture):
    camera_parking = crud.cam_park.CRUDCameraParking("test_server_db")
    item = camera_parking.read(1)
    assert item["camera_id"] == 1, "Поле не соответствует ожидаемому значению!"
    assert item["camera_url"] == "https://s1.moidom-stream.ru/camera1", "Поле не соответствует ожидаемому значению!"
    assert item["coords"] == [61, 34], "Поле не соответствует ожидаемому значению!"
    assert item["parking_places"] == [[329, 179], [308, 193], [924, 374]], "Поле не соответствует ожидаемому значению!"


def test_delete(cam_park_fixture):
    camera_parking = crud.cam_park.CRUDCameraParking("test_server_db")
    deleted_item = camera_parking.delete(1)
    assert deleted_item["camera_id"] == 1, "Возвращен элемент не соответствующий удаляемому!"
    response_list = camera_parking.read_all()
    assert len(response_list) == 2, "Количество элементов после удаления не соответствует ожидаемому числу!"
    for item in response_list:
        assert item["camera_id"] != 1, "Присутствует имя удаленного элемента!"


def test_delete_all(cam_park_fixture):
    camera_parking = crud.cam_park.CRUDCameraParking("test_server_db")
    assert camera_parking.delete_all() == "Collection camera_parking dropped!", "Возникли проблемы при удалении всех " \
                                                                                "элементов! "
    assert len(camera_parking.read_all()) == 0, "Коллекция не пуста!"


def test_create(cam_park_fixture):
    camera_parking = crud.cam_park.CRUDCameraParking("test_server_db")
    item = schemas.CameraParking(
        camera_id=4,
        camera_url="https://s1.moidom-stream.ru/camera4",
        coords=[34, 45],
        parking_places=[[329, 179]],
        address="Проспект Карла Маркса, 19"
    )
    assert len(camera_parking.create(item)) == 4, "После создания элемента общее количество элементов коллекции не " \
                                                  "увеличилось! "


def test_update(cam_park_fixture):
    camera_parking = crud.cam_park.CRUDCameraParking("test_server_db")
    new_item = schemas.CameraParking(
        camera_id=2,
        camera_url="https://s1.moidom-stream.ru/camera2",
        coords=[56, 56],
        parking_places=[[56, 56], [65, 65]],
        address="Проспект Карла Маркса, 19"
    )
    new_returned_item = camera_parking.update(2, new_item)
    assert len(camera_parking.read_all()) == 3, "При обновлении элемента количество элементов коллекции изменилось!"
    assert new_returned_item == new_item, "Возвращаемый элемент не совпадает с отправленным!"
