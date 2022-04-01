from server.api.upd_api import router
# from server.detection_module import DetectionModel
from server.api import cam_park_router, park_router

from fastapi import FastAPI

# dm = DetectionModel(device='cpu')

app = FastAPI()
app.include_router(router, tags=['cars_api'])
app.include_router(cam_park_router.router, tags=['camera_parking'])
app.include_router(park_router.router, tags=['parking'])
