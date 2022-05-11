from pydantic import BaseModel


class Parking(BaseModel):
    camera_id: int
    timestamp: int
    image: str
    empty_places: list
    taken_places: list
