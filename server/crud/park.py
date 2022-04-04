from pymongo import MongoClient


def item_entity(item) -> dict:
    return {
        "camera_id": item["camera_id"],
        "timestamp": item["timestamp"],
        "image": item["image"],
        "empty_places": item["empty_places"],
        "taken_places": item["taken_places"]
    }


def items_entity(items) -> list:
    return [item_entity(item) for item in items]


class CRUDParking:
    string_connection = "mongodb://localhost:27017"

    def __init__(self):
        self.connection = MongoClient(self.string_connection)

    def create(self, item):
        self.connection.local.parking.insert_one(dict(item))
        return items_entity(self.connection.local.parking.find())

    def read_all(self):
        return items_entity(self.connection.local.parking.find())

    def read(self, camera_id):
        return item_entity(self.connection.local.parking.find_one({"camera_id": int(camera_id)}))

    def update(self, camera_id, item):
        self.connection.local.parking.find_one_and_update({"camera_id": int(camera_id)}, {
            "$set": dict(item)
        })
        return item_entity(self.connection.local.parking.find_one({"camera_id": int(camera_id)}))

    def delete(self, camera_id):
        return item_entity(self.connection.local.parking.find_one_and_delete({"camera_id": int(camera_id)}))

    def delete_all(self):
        self.connection.local.parking.drop()
        return "Collection parking dropped!"


parking = CRUDParking()
