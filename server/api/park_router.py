from fastapi import APIRouter

from server import schemas
from server import crud

router = APIRouter()

parking_repository = crud.parking


@router.get('/parking')
async def read_all():
    return parking_repository.read_all()


@router.get('/parking/{camera_id}')
async def read_one(camera_id):
    return parking_repository.read_one(camera_id)


@router.post('/parking')
async def create(item: schemas.Parking):
    return parking_repository.create(item)


@router.put('/parking/{camera_id}')
async def update(camera_id, item: schemas.Parking):
    return parking_repository.update(camera_id, item)


@router.delete('/parking/{camera_id}')
async def delete(camera_id):
    return parking_repository.delete(camera_id)
