db.auth('', '')

db = db.getSiblingDB('parking_eye')

db.createCollection("camera_parking");

db.camera_parking.insertMany([
    {
        "camera_id": 20,
        "camera_url": "https://s1.moidom-stream.ru/s/public/0000000088.m3u8",
        "address": "Проспект Карла Маркса, 19",
        "coords": [61.78749, 34.38096],
        "parking_places": [[925, 375], [880, 380], [487, 383], [531, 382],
            [634, 382], [354, 388], [259, 390], [305, 391], [400, 390]]
    },
    {
        "camera_id": 6,
        "camera_url": "https://s1.moidom-stream.ru/s/public/0000006567.m3u8",
        "address": "Краснофлотская, 20",
        "coords": [61.8022, 34.32632],
        "parking_places": [[1851, 338], [1491, 391], [436, 429], [308, 458], [1806, 469],
            [146, 485], [1714, 497], [1647, 503], [1585, 512]]
    },
    {
        "camera_id": 5,
        "camera_url": "https://s1.moidom-stream.ru/s/public/0000001415.m3u8",
        "address": "Набережная Варкауса, 21",
        "coords": [61.80657, 34.3396],
        "parking_places": [[790, 364], [781, 398], [749, 419], [672, 508], [645, 541],
            [611, 569], [572, 596], [542, 633], [508, 670], [471, 694]]
    },
]);

