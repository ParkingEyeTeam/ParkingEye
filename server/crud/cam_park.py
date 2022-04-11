from pymongo import MongoClient

from server.crud import mongo_config

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
    string_connection = mongo_config.mongo_connection_string

    def __init__(self, db):
        self.connection = MongoClient(self.string_connection)
        self.db = self.connection.get_database(db)

    def __del__(self):
        self.connection.close()

    def create(self, item):
        self.db.camera_parking.insert_one(dict(item))
        return items_entity(self.db.camera_parking.find())

    def read_all(self):
        return items_entity(self.db.camera_parking.find())

    def read(self, camera_id):
        return item_entity(self.db.camera_parking.find_one({"camera_id": int(camera_id)}))

    def update(self, camera_id, item):
        self.db.camera_parking.find_one_and_update({"camera_id": int(camera_id)}, {
            "$set": dict(item)
        })
        return item_entity(self.db.camera_parking.find_one({"camera_id": int(camera_id)}))

    def delete(self, camera_id):
        return item_entity(self.db.camera_parking.find_one_and_delete({"camera_id": int(camera_id)}))

    def delete_all(self):
        self.db.camera_parking.drop()
        return "Collection camera_parking dropped!"


camera_parking = CRUDCameraParking(mongo_config.mongo_config['db'])
