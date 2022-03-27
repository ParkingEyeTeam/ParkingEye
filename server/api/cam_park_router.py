from fastapi import APIRouter

from server import schemas
from server import crud

router = APIRouter()

camera_parking_repository = crud.camera_parking


@router.get('/camera_parking')
async def read_all():
    return camera_parking_repository.read_all()


@router.get('/camera_parking/{camera_id}')
async def read_one(camera_id):
    return camera_parking_repository.read_one(camera_id)


@router.post('/camera_parking')
async def create(item: schemas.CameraParking):
    return camera_parking_repository.create(item)


@router.put('/camera_parking/{camera_id}')
async def update(camera_id, item: schemas.CameraParking):
    return camera_parking_repository.update(camera_id, item)


@router.delete('/camera_parking/{camera_id}')
async def delete(camera_id):
    return camera_parking_repository.delete(camera_id)
