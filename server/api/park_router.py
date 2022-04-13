from fastapi import APIRouter

from server import schemas
from server import crud

router = APIRouter()

parking_repository = crud.parking


@router.get('/parking')
async def read_all():
    """
    It returns all the parking lots in the database
    :return: A list of all the parking spots in the database.
    """
    return parking_repository.read_all()


@router.get('/parking/{camera_id}')
async def read(camera_id):
    """
    > Reads the parking lot status for a given camera

    :param camera_id: The ID of the camera to read
    :return: The camera_id is being returned.
    """
    return parking_repository.read(camera_id)


@router.post('/parking')
async def create(item: schemas.Parking):
    """
    > Create a new parking item

    :param item: schemas.Parking
    :type item: schemas.Parking
    :return: The return value is a coroutine object.
    """
    return parking_repository.create(item)


@router.put('/parking/{camera_id}')
async def update(camera_id, item: schemas.Parking):
    """
    "Update a parking item in the database."


    :param camera_id: The ID of the camera that the parking spot is associated with
    :param item: schemas.Parking
    :type item: schemas.Parking
    :return: The return value is the updated item.
    """
    return parking_repository.update(camera_id, item)


@router.delete('/parking/{camera_id}')
async def delete(camera_id):
    """
    It deletes a camera from the database

    :param camera_id: The id of the camera to delete
    :return: The return value is the result of the delete function in the parking_repository.py file.
    """
    return parking_repository.delete(camera_id)


@router.delete('/parking/')
async def delete_all():
    """
    It deletes all the parking spots
    :return: The return value is the number of documents deleted.
    """
    return parking_repository.delete_all()
