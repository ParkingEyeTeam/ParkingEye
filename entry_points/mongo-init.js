db.auth('', '')

db = db.getSiblingDB('parking_eye')

db.createCollection("camera_parking");

db.camera_parking.insertMany([
    {
        "camera_id": 20,
        "camera_url":"https://s1.moidom-stream.ru/s/public/0000000088.m3u8",
        "address":"Проспект Карла Маркса, 19",
        "coords": [61.78749, 34.38096],
        "parking_places": [[329, 180], [925, 375], [880, 380], [487, 383], [531, 382],
            [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]]
    },
]);

