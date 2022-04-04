from fastapi import APIRouter

from server import schemas
from server import crud

router = APIRouter()

camera_parking_repository = crud.camera_parking

mock_items = [
    schemas.CameraParking(
        camera_id=20,
        camera_url="https://s1.moidom-stream.ru/s/public/0000000088.m3u8",
        coords=[61.78749, 34.38096],
        parking_places=[[329, 179], [308, 193], [924, 374], [879, 380], [487, 382], [531, 378],
                        [630, 378], [255, 386], [263, 390], [305, 390], [400, 386], [483, 386],
                        [531, 386], [633, 386], [354, 392], [259, 394], [400, 394]]
    ),
    schemas.CameraParking(
        camera_id=6,
        camera_url="https://s1.moidom-stream.ru/s/public/0000006567.m3u8",
        coords=[61.8022, 34.32632],
        parking_places=[[1851, 338], [1485, 391], [1495, 391], [435, 428], [436, 434], [1405, 451],
                        [303, 458], [313, 458], [1806, 464], [1806, 474], [146, 484], [146, 490], [1709, 492],
                        [1718, 492], [1647, 498], [1714, 502], [1585, 507], [1647, 508], [1580, 516], [1589, 516]]
    )]
camera_parking_repository.delete_all()

for mock_item in mock_items:
    camera_parking_repository.create(mock_item)


@router.get('/camera_parking')
async def read_all():
    return camera_parking_repository.read_all()


@router.get('/camera_parking/{camera_id}')
async def read(camera_id):
    return camera_parking_repository.read(camera_id)


@router.post('/camera_parking')
async def create(item: schemas.CameraParking):
    return camera_parking_repository.create(item)


@router.put('/camera_parking/{camera_id}')
async def update(camera_id, item: schemas.CameraParking):
    return camera_parking_repository.update(camera_id, item)


@router.delete('/camera_parking/{camera_id}')
async def delete(camera_id):
    return camera_parking_repository.delete(camera_id)


@router.delete('/camera_parking/')
async def delete_all():
    return camera_parking_repository.delete_all()
