from pydantic import BaseModel


class CameraParking(BaseModel):
    camera_id: int
    camera_url: str
    coords: list
    parking_places: list
