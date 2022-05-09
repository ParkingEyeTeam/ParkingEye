from server import crud, schemas


def test_read_all(park_fixture):
    parking = crud.park.CRUDParking("test_server_db")
    response_list = parking.read_all()
    assert len(response_list) == 3, "Количество элементов не соответствует ожидаемому числу!"


def test_read(park_fixture):
    parking = crud.park.CRUDParking("test_server_db")
    item = parking.read(20)
    assert item["camera_id"] == 20, "Поле не соответствует ожидаемому значению!"
    assert item["timestamp"] == 20140812007401, "Поле не соответствует ожидаемому значению!"
    assert item["image"] == "server/tests/server_tests/images/image20.png", "Поле не соответствует ожидаемому значению!"
    assert item["empty_places"] == [[925, 375], [880, 380], [487, 383]], "Поле не соответствует ожидаемому значению!"
    assert item["taken_places"] == [[531, 382], [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]], \
        "Поле не соответствует ожидаемому значению!"


def test_delete(park_fixture):
    item_it_to_delete = 20
    parking = crud.park.CRUDParking("test_server_db")
    deleted_item = parking.delete(item_it_to_delete)
    assert deleted_item["camera_id"] == item_it_to_delete, "Возвращен элемент не соответствующий удаляемому!"
    response_list = parking.read_all()
    assert len(response_list) == 2, "Количество элементов после удаления не соответствует ожидаемому числу!"
    for item in response_list:
        assert item["camera_id"] != item_it_to_delete, "Присутствует имя удаленного элемента!"


def test_delete_all(park_fixture):
    parking = crud.park.CRUDParking("test_server_db")
    assert parking.delete_all() == "Collection parking dropped!", "Возникли проблемы при удалении всех "\
                                                                  "элементов! "
    assert len(parking.read_all()) == 0, "Коллекция не пуста!"


def test_create(park_fixture):
    parking = crud.park.CRUDParking("test_server_db")
    item = schemas.Parking(
        camera_id=20,
        timestamp=20140812007401,
        image="server/tests/server_tests/images/image20.png",
        empty_places=[[925, 375], [880, 380], [487, 383]],
        taken_places=[[531, 382], [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]]
    )
    assert len(parking.create(item)) == 4, "После создания элемента общее количество элементов коллекции не "\
                                           "увеличилось! "


def test_update(park_fixture):
    parking = crud.park.CRUDParking("test_server_db")
    new_item = schemas.Parking(
        camera_id=20,
        timestamp=20140212007401,
        image="server/tests/server_tests/images/image20.png",
        empty_places=[[880, 380], [487, 383]],
        taken_places=[[925, 375], [531, 382], [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]]
    )
    new_returned_item = parking.update(20, new_item)
    assert len(parking.read_all()) == 3, "При обновлении элемента количество элементов коллекции изменилось!"
    assert new_returned_item == new_item, "Возвращаемый элемент не совпадает с отправленным!"
