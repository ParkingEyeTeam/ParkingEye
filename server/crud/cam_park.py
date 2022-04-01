from pymongo import MongoClient


def item_entity(item) -> dict:
    return {
        "camera_id": item["camera_id"],
        "camera_url": item["camera_url"],
        "coords": item["coords"],
        "parking_places": item["parking_places"]
    }


def items_entity(items) -> list:
    return [item_entity(item) for item in items]


class CRUDCameraParking:
    string_connection = "mongodb://localhost:27017"

    def __init__(self):
        self.connection = MongoClient(self.string_connection)

    def create(self, item):
        self.connection.local.camera_parking.insert_one(dict(item))
        return items_entity(self.connection.local.camera_parking.find())

    def read_all(self):
        return items_entity(self.connection.local.camera_parking.find())

    def read_one(self, camera_id):
        return item_entity(self.connection.local.camera_parking.find_one({"camera_id": int(camera_id)}))

    def update(self, camera_id, item):
        self.connection.local.camera_parking.find_one_and_update({"camera_id": int(camera_id)}, {
            "$set": dict(item)
        })
        return item_entity(self.connection.local.camera_parking.find_one({"camera_id": int(camera_id)}))

    def delete(self, camera_id):
        return item_entity(self.connection.local.camera_parking.find_one_and_delete({"camera_id": int(camera_id)}))


camera_parking = CRUDCameraParking()
