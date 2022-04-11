db.auth('', '')

db = db.getSiblingDB('parking_eye')

db.createCollection("camera_parking");

db.camera_parking.insertMany([
    {
        "camera_id": 20,
        "camera_url":"https://s1.moidom-stream.ru/s/public/0000000088.m3u8",
        "coords": [61.78749, 34.38096],
        "parking_places": [[329, 179], [308, 193], [924, 374], [879, 380], [487, 382], [531, 378],
            [630, 378], [255, 386], [263, 390], [305, 390], [400, 386], [483, 386],
            [531, 386], [633, 386], [354, 392], [259, 394], [400, 394]]
    },
]);

